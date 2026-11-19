from pathlib import Path
from textwrap import dedent

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(dedent(text).strip()))


def code(text):
    cells.append(nbf.v4.new_code_cell(dedent(text).strip()))


md("""
# A bounded data-quality review agent
**AI Foundations (Edward Hickman) · Udacity · Project 6 — Agentic AI Systems**

The persona is a cautious reviewer: inspect, explain and defer changes to a
human. A **single deterministic rule-based agent** chooses tools from observed
schema, stores limited per-run state and stops at explicit boundaries.
It is **not an LLM**, has no natural-language planning, and makes no API calls.
The rubric permits decision logic and does not require an LLM or paid service.
The implementation uses ordinary Python function orchestration, not an unapproved
third-party agent framework.

`DESIGN_PLAN.md` records the architecture and evaluation cases before implementation.
`agentic_system.py` contains the full runnable implementation; the notebook
displays it and executes it with the same source data and test scenarios.
AI assistance was used; Edward must review, understand and personalize the
work as required by his course's academic-integrity policy.
""")
md("""
## 1. Task, data and boundaries
Review a **registered Palmer Penguins CSV** for missing cells, repeated rows,
invalid measurement values and unexpected categories. Public field data
contain 344 penguins and eight columns, collected by Kristen Gorman and Palmer
Station LTER and distributed by Horst et al. (2020). This is a new dataset and
new workflow, not a reused capstone agent. The dataset is CC0; attribution
and pinned source details are included.

No data repairs, imputation, deletions, shell commands, network tools or external
messages are available. Structured requests accept only dataset ID `penguins`
and intent `review`; file paths and free-form instructions are not accepted.
The agent is semi-autonomous within this small decision graph: it chooses
applicable checks and terminal disposition, not open-ended goals.
""")
code("""
from pathlib import Path
import hashlib
import inspect
import json
import platform
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from IPython.display import Code, display
import agentic_system
from agentic_system import Request, ReviewAgent, ReviewTools, SUMMARY, CONFIG
from evaluate_agent import run_evaluation

ROOT = Path.cwd()
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
source = ROOT / "data/penguins.csv"
versions = {"python": platform.python_version(), "numpy": np.__version__,
            "pandas": pd.__version__}
(OUT / "runtime_versions.json").write_text(json.dumps(versions, indent=2) + "\\n")
display(versions)
display(pd.read_csv(source).head())
print("Data shape:", pd.read_csv(source).shape)
print("SHA-256:", hashlib.sha256(source.read_bytes()).hexdigest())
display(CONFIG)
""")
md("""
## 2. Architecture and design tradeoffs
Figure 1 shows request validation, the decision loop, run-local memory, the
read-only tools, their observations and terminal output. The loop is a modest
sense/decide/act pattern; agent architectures and autonomy have a broader
history than LLM tool use (Wooldridge & Jennings, 1995). One agent avoids
unnecessary coordination and makes accountability easier for this bounded task.

Memory is a fresh `RunState` for every request: completed-tool names, skipped
tools, observations, counter and event trace, plus the temporary working frame.
The returned report contains aggregates and fixed policy reasons, not raw
row values or a hidden reasoning transcript. There is no conversation history,
cross-run learning, persistent memory or general-purpose planner.
""")
code("""
fig, ax = plt.subplots(figsize=(11, 7))
ax.set(xlim=(0, 11), ylim=(0, 7))
ax.axis("off")
boxes = {
    "request": (0.3, 5.5, 2.7, 1.0, "Structured request\\ndataset • intent • budget"),
    "guard": (4.1, 5.5, 2.8, 1.0, "Request gate\\nallowlist + 1–6 tool calls"),
    "memory": (0.3, 2.9, 2.7, 1.5, "Per-run memory\\nobservations + completed\\nskipped + counter + trace\\ntemporary working frame"),
    "policy": (4.1, 3.0, 2.8, 1.3, "Rule-based decision loop\\nselect next applicable tool\\nor stop; never repeat"),
    "tools": (8.0, 2.8, 2.7, 1.8, "Read-only tool dispatcher\\nload • profile • missing\\nduplicates • numeric\\ncategories"),
    "result": (3.8, 0.4, 3.4, 1.3, "Aggregate review + event trace\\ncompleted / blocked / failed\\nor budget exhausted\\nhuman decides any changes"),
}
for key, (x, y, w, h, label) in boxes.items():
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06",
                           edgecolor="#154C75", facecolor="#8CCEDE" if key == "policy" else "#F5F5F5")
    ax.add_patch(patch)
    ax.text(x+w/2, y+h/2, label, ha="center", va="center", fontsize=10)

def arrow(start, end, label="", label_position=None, curve=0):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=14,
                                connectionstyle=f"arc3,rad={curve}", color="#154C75"))
    if label_position:
        ax.text(*label_position, label, fontsize=9, ha="center", va="center",
                bbox={"facecolor": "white", "edgecolor": "none", "pad": 1})

arrow((3.05, 6.0), (4.02, 6.0))
arrow((5.5, 5.4), (5.5, 4.4), "accepted", (6.1, 4.9))
arrow((4.0, 3.9), (3.1, 3.9), "observe", (3.55, 4.12))
arrow((3.1, 3.25), (4.0, 3.25), "read state", (3.55, 2.98))
arrow((7.0, 3.95), (7.9, 3.95), "invoke", (7.45, 4.18))
arrow((7.9, 3.2), (7.0, 3.2), "result/error", (7.45, 2.96))
arrow((5.5, 2.9), (5.5, 1.8), "finish / failure / budget", (5.5, 2.3))
arrow((6.95, 5.9), (7.3, 1.1), "blocked", (8.15, 5.3), curve=-0.35)
ax.text(9.35, 1.8, "Pinned local CSV only\\nNo edit, network or shell tools",
        ha="center", fontsize=9)
fig.suptitle("Figure 1 — bounded reviewer architecture and actual control flow", fontsize=14)
fig.tight_layout()
fig.savefig(OUT / "architecture_diagram.png", dpi=180, bbox_inches="tight")
plt.show()
""")
md("""
## 3. Full implementation and decision policy
The source below is the complete implementation supplied as `agentic_system.py`,
not pseudocode. The notebook imports and runs this same module.

Policy order is load → profile → missingness → duplicates → applicable numeric
and category checks → finish. Applicability is decided from observed columns.
Completed-tool state prevents repeats; skips are explicit events. Failure stops
the run, and incomplete checks can never produce `configured_checks_clear`.
Missingness uses `isna()`, rather than equality with NaN (pandas development team,
n.d.). Positive finite numeric rules are deliberately narrow, not biological
plausibility checks.
""")
code("""
display(Code(inspect.getsource(agentic_system), language="python"))
""")
md("""
## 4. Original-data execution and observable decisions
Each trace entry reports a policy action, short reason and observed/requested
outcome. This is an inspectable rule trace, **not an LLM's private reasoning**.
The data remain unchanged. A human-review recommendation never grants the agent
permission to repair a file.
""")
code("""
before = hashlib.sha256(source.read_bytes()).hexdigest()
original = ReviewAgent().run(Request())
print("Status:", original["status"])
print("Disposition:", original["disposition"])
print("Findings:", original["findings"])
display(original["observations"])
display(pd.DataFrame(original["trace"]))
assert before == hashlib.sha256(source.read_bytes()).hexdigest()
""")
md("""
## 5. Representative scenarios and deliberate failures
The twelve cases were specified in the design plan. Only `original` is
unmodified field data. The harness explicitly constructs complete-case,
duplicate, negative-mass, categories-only, empty, instruction-text and absurd-mass
fixtures from copies; these are **test alterations**, not discovered field
observations. It also submits blocked requests, restricts a call budget and
injects a numeric-tool failure. No fixture preparation is an agent action.
""")
code("""
results, evaluation = run_evaluation(OUT / "runs")
display(evaluation)
for name in ["categories_only", "low_budget", "tool_failure", "instruction_text"]:
    result = results[name]
    print("\\nSCENARIO:", name, "—", result["status"], "/", result["disposition"])
    display(pd.DataFrame(result["trace"]))
    display(result["observations"])
""")
md("""
## 6. Evaluation, limitations and responsible use
The original 344-row CSV yields 19 missing cells across 11 records: two in
each of four measurements and eleven in `sex`. Six tool calls complete and
the result is `human_review`; no repeated rows or configured numeric/category
violations are found. Missing cells and affected records are different counts.

The categories-only fixture skips numeric validation based on profile state.
It also shows why repeated attribute rows need interpretation: dropping
measurement columns makes many animals share the same remaining attributes;
this does **not** establish duplicate penguins. The low-budget case stops after
load and profile with `incomplete_review`, not a success claim. Injected numeric
failure stops before category checking; this is a simulated outage, not a
failure of pandas in the original-data run.

The instruction-like species text is never executed or sent to an LLM; it is
counted as an unexpected category. This verifies a narrow data/control separation,
not general prompt-injection resistance. Most importantly, the complete-case
fixture with **999,999 g body mass is not flagged** by positivity-only rules.
The reported `configured_checks_clear` is correct for those rules but would be
misleading if treated as a scientific quality certificate. This known miss is
retained, not relabeled as a robustness success.

All twelve predeclared policy expectations are observed, including that known
miss; this is not 100% anomaly detection, real-world accuracy or comprehensive
safety assurance. Read-only tools, a six-call ceiling, no automatic repairs and
explicit terminal statuses support limited control and accountability, consistent
with risk-management principles rather than certification (NIST, 2023).
The human should investigate missingness rather than silently delete records,
which could alter species, island or sex representation. The notebook uses
public animal data, but aggregate-only logging alone would not establish privacy
for a future sensitive dataset. No OS sandbox, adversarial resource test,
wall-clock timeout or automatic recovery from arbitrary programming bugs is claimed.
""")
md("""
## References
Horst, A. M., Hill, A. P., & Gorman, K. B. (2020).
*palmerpenguins: Palmer Archipelago (Antarctica) penguin data* [Data set].
https://doi.org/10.5281/zenodo.3960218

National Institute of Standards and Technology. (2023).
*Artificial intelligence risk management framework (AI RMF 1.0)*
(NIST AI 100-1). https://doi.org/10.6028/NIST.AI.100-1

pandas development team. (n.d.). *Working with missing data*.
https://pandas.pydata.org/docs/user_guide/missing_data.html

Wooldridge, M., & Jennings, N. R. (1995). Intelligent agents: Theory and practice.
*The Knowledge Engineering Review, 10*(2), 115–152.
https://doi.org/10.1017/S0269888900008122
""")
from sys import path
path.insert(0, str(ROOT))
from agentic_system import SUMMARY

md("## Notebook summary\n\n" + SUMMARY)
notebook = nbf.v4.new_notebook(cells=cells)
notebook.metadata.kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
notebook.metadata.language_info = {"name": "python", "version": "3.11.18"}
nbf.write(notebook, ROOT / "agentic_system.ipynb")
