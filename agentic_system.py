"""Bounded, rule-based data-quality reviewer; no LLM, network or data editing."""
from dataclasses import dataclass, field
import hashlib
import io
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "config.json").read_text())
SOURCE_SHA256 = "f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93"
PERSONA = "Cautious data-quality reviewer: inspect, explain and defer changes to a human."


class ToolFailure(Exception):
    pass


@dataclass(frozen=True)
class Request:
    dataset_id: str = "penguins"
    intent: str = "review"
    max_tool_calls: int = 6


@dataclass
class RunState:
    observations: dict = field(default_factory=dict)
    completed: list = field(default_factory=list)
    skipped: list = field(default_factory=list)
    events: list = field(default_factory=list)
    tool_calls: int = 0
    frame: pd.DataFrame | None = None

    def log(self, action, reason, outcome):
        self.events.append({"sequence": len(self.events) + 1,
                            "action": action, "reason": reason, "outcome": outcome})


class ReviewTools:
    """Read-only functions; fixture input and fault injection are test seams."""

    def __init__(self, fixture=None, fail_tool=None):
        self.fixture = fixture
        self.fail_tool = fail_tool

    def dispatch(self, name, state):
        tools = {"load": self.load, "profile": self.profile,
                 "missing": self.missing, "duplicates": self.duplicates,
                 "numeric": self.numeric, "categories": self.categories}
        if name not in tools:
            raise ToolFailure("Tool is not allowlisted")
        if self.fail_tool == name:
            raise ToolFailure("Injected tool failure for evaluation")
        return tools[name](state)

    def load(self, state):
        if self.fixture is None:
            path = ROOT / CONFIG["relative_path"]
            if path.stat().st_size > CONFIG["max_bytes"]:
                raise ToolFailure("Input exceeds byte limit")
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
                raise ToolFailure("Original dataset fingerprint mismatch")
            frame = pd.read_csv(io.BytesIO(raw))
        else:
            frame = self.fixture.copy(deep=True)
        if not 0 < len(frame) <= CONFIG["max_rows"]:
            raise ToolFailure("Input row count is empty or exceeds limit")
        if not 0 < len(frame.columns) <= CONFIG["max_columns"] or not frame.columns.is_unique:
            raise ToolFailure("Invalid column count or repeated column names")
        if not all(isinstance(c, str) and len(c) <= 100 for c in frame.columns):
            raise ToolFailure("Invalid column labels")
        state.frame = frame
        return {"rows": len(frame), "columns": len(frame.columns),
                "source": "explicit evaluation fixture" if self.fixture is not None else "pinned public CSV"}

    def profile(self, state):
        columns = list(state.frame.columns)
        return {"missing_columns": sorted(set(CONFIG["required_columns"]) - set(columns)),
                "extra_column_count": len(set(columns) - set(CONFIG["required_columns"])),
                "measurement_columns": [c for c in CONFIG["measurement_columns"] if c in columns],
                "category_columns": [c for c in CONFIG["categories"] if c in columns]}

    def missing(self, state):
        counts = state.frame.isna().sum()
        return {"missing_cells": int(counts.sum()),
                "rows_with_missing": int(state.frame.isna().any(axis=1).sum()),
                "by_column": {c: int(counts[c]) for c in CONFIG["required_columns"] if c in counts}}

    def duplicates(self, state):
        return {"repeated_rows_after_first": int(state.frame.duplicated().sum())}

    def numeric(self, state):
        counts = {}
        for column in state.observations["profile"]["measurement_columns"]:
            raw = state.frame[column]
            values = pd.to_numeric(raw, errors="coerce")
            invalid = raw.notna() & (values.isna() | ~np.isfinite(values) | (values <= 0))
            counts[column] = int(invalid.sum())
        return {"invalid_cells": sum(counts.values()), "by_column": counts,
                "policy": "Nonmissing measurement must be numeric, finite and positive; no biological upper bounds."}

    def categories(self, state):
        counts = {}
        for column in state.observations["profile"]["category_columns"]:
            raw = state.frame[column]
            counts[column] = int((raw.notna() & ~raw.isin(CONFIG["categories"][column])).sum())
        return {"unexpected_cells": sum(counts.values()), "by_column": counts}


class ReviewAgent:
    def __init__(self, tools=None):
        self.tools = tools if tools is not None else ReviewTools()

    def decide(self, state):
        for name, reason in [
            ("load", "No dataset is loaded; use the registered read-only source."),
            ("profile", "Loaded data require a schema observation before selecting checks."),
            ("missing", "Count missing values without deleting or filling them."),
            ("duplicates", "Check repeated attribute rows without assuming duplicate animals."),
        ]:
            if name not in state.completed:
                return name, reason
        profile = state.observations["profile"]
        for tool, key in [("numeric", "measurement_columns"), ("categories", "category_columns")]:
            if tool not in state.completed and tool not in state.skipped:
                if profile[key]:
                    return tool, f"Profile contains applicable {key}; run the bounded check."
                state.skipped.append(tool)
                state.log("skip_" + tool, f"No applicable {key} were observed.", "skipped")
        return None, "All applicable configured checks completed."

    def run(self, request):
        state = RunState()

        def finish(status, reason):
            state.log("finish", reason, status)
            findings = []
            o = state.observations
            if o.get("profile", {}).get("missing_columns"):
                findings.append("required_columns_missing")
            if o.get("profile", {}).get("extra_column_count", 0):
                findings.append("unrecognized_columns")
            if o.get("missing", {}).get("missing_cells", 0):
                findings.append("missing_values")
            if o.get("duplicates", {}).get("repeated_rows_after_first", 0):
                findings.append("repeated_rows")
            if o.get("numeric", {}).get("invalid_cells", 0):
                findings.append("invalid_measurements")
            if o.get("categories", {}).get("unexpected_cells", 0):
                findings.append("unexpected_categories")
            disposition = ("incomplete_review" if status != "completed" else
                           "human_review" if findings else "configured_checks_clear")
            return {"status": status, "disposition": disposition, "reason": reason,
                    "findings": findings, "tool_calls": state.tool_calls,
                    "completed_tools": state.completed, "skipped_tools": state.skipped,
                    "observations": o, "trace": state.events,
                    "data_modified": False,
                    "scope": "Configured checks only; not scientific validation or a quality certificate."}

        if not isinstance(request, Request):
            return finish("blocked", "Expected a structured Request, not free-form instructions.")
        if request.dataset_id != CONFIG["dataset_id"] or request.intent != "review":
            return finish("blocked", "Only the registered dataset and review intent are allowed.")
        if type(request.max_tool_calls) is not int or not 1 <= request.max_tool_calls <= CONFIG["max_tool_calls"]:
            return finish("blocked", "Tool budget must be an integer from one to six.")
        while True:
            name, reason = self.decide(state)
            if name is None:
                return finish("completed", reason)
            if state.tool_calls >= request.max_tool_calls:
                return finish("budget_exhausted", "Next required tool would exceed the call budget.")
            if name in state.completed:
                return finish("failed", "Repeated-tool guard triggered.")
            state.tool_calls += 1
            state.log(name, reason, "requested")
            try:
                observation = self.tools.dispatch(name, state)
            except (ToolFailure, OSError, pd.errors.ParserError, UnicodeError, ValueError, TypeError):
                state.log(name, "Tool failed; no retry or success inference.", "error")
                return finish("failed", "Tool failure; remaining checks were not performed.")
            state.observations[name] = observation
            state.completed.append(name)
            state.log(name, "Aggregate observation saved in this run's state.", "observed")


if __name__ == "__main__":
    print(json.dumps(ReviewAgent().run(Request()), indent=2, allow_nan=False))


SUMMARY = (
    "This single rule-based agent reviews a registered public penguin dataset with "
    "read-only tools, a bounded decision loop and per-run state. "
    "On the original data it completes six tool calls and sends missing-value findings "
    "for human review without changing a record. "
    "Designed evaluation cases exercise conditional tool skipping, duplicate and invalid-value "
    "flags, blocked requests, budget exhaustion and a simulated tool failure. "
    "A positive but absurd body mass exposes a deliberate limitation of the positivity-only "
    "measurement rule rather than demonstrating scientific validation. "
    "The workflow has no LLM, general-language planning or persistent memory and cannot "
    "certify data quality, infer causality or replace a domain expert."
)
