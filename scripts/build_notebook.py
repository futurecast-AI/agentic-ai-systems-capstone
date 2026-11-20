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
# An LLM-directed, bounded data-quality review agent
**AI Foundations (Edward Hickman) · Udacity · Project 6 resubmission**

This revision replaces the rejected rule-based controller with **MiniMax-M3,
LangChain and LangGraph**. A language model interprets the user's instruction,
chooses a tool, reads its observation and decides again. Python enforces
capability limits; it does not supply the checking sequence.

The notebook displays the complete implementation, **makes a real live model
run**, and inspects eight separately captured live scenarios. Scripted unit
tests are distinguished from real provider evidence. Replit AI assisted with
implementation, debugging, evaluation and writing. Edward must understand,
review and personalize the work under the course's AI-use policy; independent
authorship and reviewer acceptance are not claimed.
""")
md("""
## 1. Task and data

The persona is a cautious reviewer of one registered public Palmer Penguins CSV.
It may inspect but cannot repair, delete, run shell commands or send messages.
The source has 344 rows and eight columns; it is distributed by Horst et al.
(2020), with field data from Kristen Gorman and Palmer Station LTER.
`data/DATA_NOTICE.md` records CC0 attribution, source version and fingerprint.

Structured request validation restricts dataset, intent and budget.
**Natural-language instructions remain free-form within that scope**: missingness,
duplicates, a full review, or a request the model must refuse.
User instructions and aggregate tool observations go to the model provider.
Raw dataset rows are not sent by the registered tools.
""")
code("""
from pathlib import Path
import hashlib
import inspect
import json
import platform
from importlib.metadata import version
import pandas as pd
from IPython.display import Code, Image, display
import agentic_system
from agentic_system import CONFIG, PERSONA, Request, ReviewAgent, SUMMARY

ROOT = Path.cwd()
OUT = ROOT / "outputs"
source = ROOT / "data/penguins.csv"
versions = {"python": platform.python_version(),
            **{p: version(p) for p in ["langgraph", "langchain-openai", "langchain-core", "pandas"]}}
(OUT / "runtime_versions.json").write_text(json.dumps(versions, indent=2) + "\\n")
display(versions)
print("Shape:", pd.read_csv(source).shape)
print("Source SHA-256:", hashlib.sha256(source.read_bytes()).hexdigest())
display(CONFIG)
""")
md("""
## 2. Architecture: fixed graph, model-selected actions

LangGraph supplies state, nodes and transitions (LangChain, n.d.). Its graph
alternates `llm_decision` and `read_only_tool`. The graph is fixed, but the
**identity, relevance and order of analysis tools are chosen by the LLM**.
The loop is inspired by interleaved language-model action and observation
(Yao et al., 2023), not a reproduction of the ReAct benchmark.

Every run has fresh message history, aggregate observations, completed tools,
counters, event trace and a local working frame. The LLM sees messages, not
the frame. There is no persistent memory, multi-agent team or cross-run learning.
Public tool justifications are not private chain-of-thought.
""")
code("""
display(Image(filename=str(OUT / "architecture_diagram.png")))
print(PERSONA)
""")
md("""
## 3. Complete runnable implementation

The following is the actual imported source, not pseudocode or an unused model
client. `create_model` uses the key from the environment; the value is never
displayed. MiniMax's OpenAI-compatible endpoint is used through LangChain
(MiniMax, n.d.). Six read-only function schemas are bound to the model.
""")
code("""
display(Code(inspect.getsource(agentic_system), language="python"))
""")
md("""
## 4. Execute a genuine LLM reasoning/action/observation loop

This cell makes paid/provider-metered requests and requires `MINIMAX_API_KEY`
in the execution environment. No fake or deterministic fallback is available.
The model chooses the analysis actions for this narrow request. Running the
notebook again may produce different wording or tool paths.
""")
code("""
live_demo = ReviewAgent().run(Request(
    instructions="Report only missing-data counts for this CSV. Do not run unrelated checks."))
assert any(m["role"] == "ai" for m in live_demo["messages"]), "No real model response."
assert live_demo["status"] == "completed", "Inspect the unsuccessful live run."
assert "missing" in live_demo["observations"], "Missingness evidence was not obtained."
(OUT / "notebook_live_demo.json").write_text(json.dumps(live_demo, indent=2) + "\\n")
display({k: live_demo[k] for k in [
    "provider", "model", "status", "disposition", "model_turns", "tool_calls", "completed_tools"]})
display(pd.DataFrame(live_demo["trace"]))
print(live_demo["answer"])
""")
md("""
### See the observations return before subsequent decisions

The transcript alternates LLM-selected actions and actual tool results.
The `reason` arguments are short public justifications. They are observable
outputs, not proof of the model's hidden internal reasoning.
""")
code("""
for message in live_demo["messages"]:
    if message["role"] in ["system", "human"]:
        continue
    print("\\nROLE:", message["role"])
    if message.get("tool_calls"):
        print("MODEL-SELECTED:", message["tool_calls"])
    else:
        print(message["content"])
""")
md("""
## 5. Eight captured live scenarios

`evaluate_agent.py` made real provider calls for each case below. This cell
**reads saved evidence**, rather than pretending to execute all eight again.
The manifest fingerprints the evaluated implementation and configuration.
These are designed development cases, not a blinded or statistically
representative reliability benchmark. Fixtures are deliberately altered copies.
""")
code("""
evaluation = pd.read_csv(OUT / "llm_runs/evaluation_summary.csv").fillna("")
display(evaluation[["scenario", "status", "disposition", "model_turns", "tool_calls"]])
manifest = json.loads((OUT / "llm_runs/run_manifest.json").read_text())
assert manifest["implementation_sha256"] == hashlib.sha256((ROOT / "agentic_system.py").read_bytes()).hexdigest()
assert manifest["evaluator_sha256"] == hashlib.sha256((ROOT / "evaluate_agent.py").read_bytes()).hexdigest()
assert manifest["config"] == CONFIG
display(manifest)
runs = {name: json.loads((OUT / "llm_runs" / f"{name}.json").read_text())
        for name in evaluation.scenario}
assert all(r["provider"] == "minimax" and r["evidence_type"] == "live_provider_response"
           for r in runs.values())
display(pd.DataFrame([{"request": name, "path": " -> ".join(r["completed_tools"]),
                      "status": r["status"], "coverage": r["full_configured_coverage"]}
                     for name, r in runs.items()]))
""")
md("""
## 6. Failure, budget and write-request boundaries

The low-budget case may stop before a third tool. The injected numeric failure
returns an error observation to the LLM so it can explain the missing evidence.
There is no repair or deletion tool, even when natural language asks for one.
Completion, full configured coverage and scientific validity are different.
""")
code("""
for name in ["low_budget", "tool_failure", "delete_request"]:
    r = runs[name]
    print("\\nSCENARIO:", name)
    display({k: r[k] for k in ["status", "disposition", "tool_calls", "model_turns", "data_modified"]})
    display(pd.DataFrame(r["trace"]))
    print("MODEL ANSWER:", r["answer"] or "(No final model answer; the guard stopped the run.)")
""")
md("""
## 7. Known miss and fallible explanations

The `absurd_positive_mass` fixture has 333 complete rows and a manually inserted
999,999 g value. The numeric tool reports only finite/positive validity counts;
it does not return the actual mass. **The model cannot see that hidden outlier
through those observations.** A clear configured check is not a scientific
certificate.

Early real runs are retained under `outputs/development_attempts`. One batch
request was stopped; the guard now rejects the batch and lets the model choose
one action. Another development run overinterpreted projected attribute repeats
and marginal missing counts. Instructions were strengthened, not the saved
answers edited. The final explanation audit records remaining limitations.
""")
code("""
known = runs["absurd_positive_mass"]
display(known["observations"])
print("Disposition:", known["disposition"])
print(known["answer"])
print("\\nEXPLANATION AUDIT")
display(json.loads((OUT / "explanation_audit.json").read_text()))
""")
md("""
## 8. Safety, reproducibility and responsible use

Allowlisted tools, schema validation, source fingerprint, size bounds, six tool
executions, twelve model turns, a client timeout setting and zero automatic
provider retries constrain this small system. Invalid tools or dependencies stop;
a rejected batch returns feedback without running any requested tool.
These are risk controls, not NIST certification (NIST, 2023).

There is no OS isolation, end-to-end time/cost guarantee, persistent memory,
general prompt-injection defense, scientific range validation or fairness study.
User text reaches a third party. Aggregate outputs alone do not guarantee privacy.
The harness writes evaluation artifacts; registered agent tools cannot write data.

`outputs/validation.txt` records offline unit tests with a scripted model.
They check software assertions and do **not** establish live LLM planning,
scientific accuracy or a general success rate. Seeds/fingerprints/package freezes
do not remove provider nondeterminism.
""")
code("""
print((OUT / "validation.txt").read_text())
display(json.loads((OUT / "llm_runs/source_integrity.json").read_text()))
assert hashlib.sha256(source.read_bytes()).hexdigest() == agentic_system.SOURCE_SHA256
assert all(not r["data_modified"] for r in runs.values())
print("Source fingerprint unchanged; all recorded agent runs report no data modification.")
""")
md("""
## References

Horst, A. M., Hill, A. P., & Gorman, K. B. (2020). *palmerpenguins: Palmer Archipelago
(Antarctica) penguin data* [Data set]. https://doi.org/10.5281/zenodo.3960218

LangChain. (n.d.). *Workflows and agents*.
https://docs.langchain.com/oss/python/langgraph/workflows-agents

MiniMax. (n.d.). *OpenAI API compatibility*.
https://platform.minimax.io/docs/api-reference/text-openai-api

National Institute of Standards and Technology. (2023). *Artificial intelligence
risk management framework (AI RMF 1.0)*. https://doi.org/10.6028/NIST.AI.100-1

Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023).
ReAct: Synergizing reasoning and acting in language models. *International
Conference on Learning Representations*. https://openreview.net/forum?id=WE_vluYUL-X
""")
from sys import path
path.insert(0, str(ROOT))
md("""
## Notebook summary

This single LLM-directed reviewer uses LangGraph to alternate model decisions
with six read-only tool capabilities and fresh message memory.
In the full live review, it made six tool executions and found 19 missing cells
across 11 records; narrower requests produced shorter model-selected paths.
The budget case stopped incomplete, an injected error returned to the model for
explanation, and the unsupported deletion request used no tools.
The positive 999,999 g fixture still passed the limited numeric rule, while
the explanation audit retained arithmetic and coverage errors in model prose.
The evidence demonstrates a bounded action/observation loop, not hallucination-free
reasoning, scientific validity, independent authorship or deployment readiness.
""")
notebook = nbf.v4.new_notebook(cells=cells)
notebook.metadata.kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
notebook.metadata.language_info = {"name": "python", "version": "3.11.18"}
nbf.write(notebook, ROOT / "agentic_system.ipynb")
