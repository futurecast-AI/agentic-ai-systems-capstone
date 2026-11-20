# Response to “Required Improvements — Agentic AI Implementation”

The reviewer was correct: the original implementation was a deterministic
checklist and did not demonstrate the required LLM-directed architecture.
This revision replaces that planner.

| Required improvement | Revised implementation | Actual evidence |
|---|---|---|
| Real LLM integration | `create_model`, ChatOpenAI, MiniMax-M3 | Current transcripts include provider model, response identifiers and usage |
| LangChain/LangGraph | `StateGraph(AgentState)` and bound function schemas | Full implementation shown and imported in executed notebook |
| Interpret user instructions | `Request.instructions` passed as a HumanMessage | Missingness-only and duplicates-only produced different short plans |
| Dynamic tool selection | `_ask` returns model-selected calls; `_execute` validates them | `load → missing` versus `load → duplicates` versus the full review |
| Observe and decide again | ToolMessages appended with `add_messages`, then another model turn | Original run: seven model turns, six tool executions |
| Persona | Cautious, read-only reviewer in `PERSONA` | Prompt retained in each transcript |
| Memory/state | AgentState messages and fresh RunState | Observations, completed tools, counters, temporary frame and ordered trace |
| Safety/failure behavior | Allowlist, budgets, prerequisites, no editing tools | Two-call stop, explained injected error, zero-tool deletion refusal |

The graph's control topology is fixed; **the analytical actions are not**.
Python does not map instruction keywords to a sequence or choose a replacement
tool. When an early model response requested two tools at once, the guard
blocked it. The revised guard returns rejection observations; the model itself
must choose one tool. Repeated rejection cannot exceed the model-turn ceiling.

## What is not claimed

The eight cases are designed development examples, not a held-out reliability
benchmark. Fifty-two offline unit tests use scripted responses and are labeled
separately. No claim of 100% correct explanations, safety or scientific validity
is made. The report/audit preserve a numerical wording error and unsupported
coverage recommendation in the final model response, plus the deliberately
undetectable positive-mass fixture.

## Files to review

1. `module_summary.pdf`: revised report and source-backed limitations.
2. `agentic_system.ipynb`: executed source and real action/observation demo.
3. `outputs/llm_runs/`: current eight-case CSV, transcripts and source manifest.
4. `outputs/explanation_audit.json`: retained model errors.
5. `agentic_system.py`, `config.json`, `requirements.txt`, `tests/`: runnable work.

AI assistance is disclosed. Edward must understand/personalize the work under
course policy. This response does not claim a passing decision or classroom upload.
