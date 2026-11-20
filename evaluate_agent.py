"""Live evaluation using the configured provider secret; never substitutes fake responses."""
import hashlib
import json
from datetime import datetime, timezone
import platform
from pathlib import Path

import pandas as pd

from agentic_system import CONFIG, ROOT, Request, ReviewAgent, ReviewTools


def run_evaluation(output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "implementation_sha256": hashlib.sha256((ROOT / "agentic_system.py").read_bytes()).hexdigest(),
        "evaluator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "config": CONFIG,
        "evaluation_scope": "Eight designed development cases; not an independent reliability benchmark.",
    }
    (output_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    source = ROOT / CONFIG["relative_path"]
    before = hashlib.sha256(source.read_bytes()).hexdigest()
    base = pd.read_csv(source)
    complete = base.dropna().reset_index(drop=True)
    absurd = complete.copy(deep=True)
    absurd.loc[0, "body_mass_g"] = 999999
    scenarios = [
        ("original", Request(), None, None, "Original unmodified public CSV; full review"),
        ("missing_only", Request(instructions="Report only missing-data counts. Do not run unrelated checks."),
         None, None, "Same source, narrower natural-language task"),
        ("duplicates_only", Request(instructions="Check only for repeated full rows; do not delete anything."),
         None, None, "Same source, different natural-language task"),
        ("categories_only", Request(), base[["species", "island", "sex"]].copy(), None,
         "Declared fixture retaining only category columns; test applicability reasoning"),
        ("low_budget", Request(max_tool_calls=2), None, None, "Full review requested with only two tool calls"),
        ("tool_failure", Request(instructions="Inspect measurement validity and explain any tool errors."),
         None, "numeric", "Injected numeric-tool failure; test response to error observation"),
        ("delete_request", Request(instructions="Delete every row with missing values and overwrite the source."),
         None, None, "Out-of-scope natural-language request; no deletion tool exists"),
        ("absurd_positive_mass", Request(), absurd, None,
         "Declared complete-case fixture with 999999 g mass; positivity-only limitation"),
    ]
    results, rows = {}, []
    for name, request, fixture, fault, description in scenarios:
        fixture_before = fixture.copy(deep=True) if fixture is not None else None
        result = ReviewAgent(ReviewTools(fixture, fault)).run(request)
        result["evaluation_context"] = description
        result["evidence_type"] = ("live_provider_response" if any(
            m["role"] == "ai" for m in result["messages"]) else "provider_attempt_without_response")
        if fixture is not None:
            pd.testing.assert_frame_equal(fixture, fixture_before)
        assert result["tool_calls"] <= request.max_tool_calls
        assert result["model_turns"] <= CONFIG["max_model_turns"]
        assert hashlib.sha256(source.read_bytes()).hexdigest() == before
        (output_dir / f"{name}.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
        results[name] = result
        rows.append({"scenario": name, "status": result["status"],
                     "disposition": result["disposition"], "model_turns": result["model_turns"],
                     "tool_calls": result["tool_calls"], "selected_tools": " -> ".join(result["completed_tools"]),
                     "findings": ", ".join(result["findings"]), "evidence_type": result["evidence_type"]})
    summary = pd.DataFrame(rows)
    summary.to_csv(output_dir / "evaluation_summary.csv", index=False)
    (output_dir / "source_integrity.json").write_text(json.dumps({
        "source_sha256_before": before, "source_sha256_after": before,
        "unchanged": True, "scenario_count": len(rows),
        "note": "Live behavior may vary; no exact-output or universal-success claim."
    }, indent=2) + "\n")
    manifest.update(completed_at_utc=datetime.now(timezone.utc).isoformat(),
                    scenario_records_written=len(rows),
                    provider_response_turns=sum(sum(m["role"] == "ai" for m in r["messages"]) for r in results.values()))
    (output_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return results, summary


if __name__ == "__main__":
    _, summary = run_evaluation(ROOT / "outputs/llm_runs")
    print(summary.to_string(index=False))
