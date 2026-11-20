# LLM-directed agentic workflows capstone — resubmission

**AI Foundations (Edward Hickman) · Udacity · Project 6**

The rejected deterministic controller has been replaced with **MiniMax-M3,
LangChain and LangGraph**. Eight real provider-backed scenarios, a separately
executed notebook demo, a revised APA report and source are included.
This is prepared for Edward's review and resubmission—not a classroom pass,
independent-authorship claim or production deployment.

## Start here

- `module_summary.pdf`: revised nine-page report, including architecture,
  actual behavior, plain-language explanation, limitations and references.
- `agentic_system.ipynb`: executed notebook with full source, a genuine live
  demo, saved-case inspection and a five-sentence conclusion.
- `agentic_system.py`: runnable LLM agent; `evaluate_agent.py`: actual live suite.
- `outputs/llm_runs/`: current unedited model/tool transcripts and provenance.
- `outputs/explanation_audit.json`: retained errors and scope limits.
- `REVIEWER_RESPONSE.md`: maps each requested improvement to code and evidence.

Opening the report, HTML notebook or saved traces does not need an API key.
**Rerunning live calls needs an active, funded text-API account.**

## What is genuinely agentic?

`user instructions → LLM action → guarded tool → ToolMessage → LLM next action/final answer`

The fixed LangGraph topology does not prescribe the checking sequence.
The model, not a keyword planner or Python checklist, selects tool identities,
order and when to answer. Six deterministic tools perform the requested
computations; deterministic tools are not the same as a deterministic planner.

| Component | Implementation |
|---|---|
| Persona | Cautious reviewer in `PERSONA` |
| Reasoning/decisions | Real model-selected calls and public action justifications |
| Tools | load, profile, missing, duplicates, numeric, categories |
| Memory/state | Fresh message history, observations, completed tools, counters, trace and local frame |
| Feedback | Actual observations and rejected-batch/error messages return to the LLM |
| Authority | Read-only registered CSV; no editing, shell or arbitrary-path tools |

Public justifications are not hidden chain-of-thought. Optional MiniMax thinking
output is disabled; this does not replace the model's observable tool decisions.
There is no persistent memory or cross-run learning.

## Actual observed behavior

The full review used six tool executions and seven model turns, finding
**19 missing cells across 11 records** in the 344×8 source.
Missingness-only selected `load → missing`; duplicates-only selected
`load → duplicates`. The two-call budget stopped incomplete, an injected
numeric fault was explained after an error observation, and the unsupported
deletion request was refused with **zero tool executions**.

Do not equate completion with correctness:

- A 999,999 g fixture still passes the finite/positive numeric rule.
- The model sometimes overstates its evidence. The final original-data answer
  contains a ratio error and contradicts its own missingness table in its closing
  recommendation. The audit preserves these errors; answers were not edited.
- The reduced-schema case made an unnecessary numeric call with no measurement
  columns. Its empty result is not measurement validation.
- Eight designed development cases and 52 passing offline tests are not a
  general success rate, hallucination-free guarantee or scientific validation.

An early live request batched two tools despite the provider setting. The guard
now executes neither and returns rejection observations so the LLM can choose
one itself. Repeated rejections are bounded by twelve model turns.
Six tool executions remain the maximum. Client timeout settings and zero
automatic provider retries are not an end-to-end runtime/cost guarantee.

## Setup and run

Tested with Python 3.11.18. `requirements.txt` is the actual environment freeze.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest tests -q
```

Supply `MINIMAX_API_KEY` through environment configuration or a secure Secrets
manager; never put its value in source, notebooks, logs or the submission.
The default model is `MiniMax-M3`, endpoint `https://api.minimax.io/v1`.

```bash
python agentic_system.py
python evaluate_agent.py
```

For explicitly selected OpenAI access, set `AGENT_LLM_PROVIDER=openai` and supply
`OPENAI_API_KEY`; configured model: `gpt-4.1-mini`. That alternative is
unit-tested, but successful live evidence in this revision is MiniMax-only.
No automatic provider/key substitution or fake fallback exists.

```python
from agentic_system import Request, ReviewAgent
result = ReviewAgent().run(Request(instructions="Report only missing data."))
```

Live requests may incur charges. User instructions and aggregate observations
reach the provider; local dataset frames are not sent by these tools.

## Reproduce or inspect

See `REPRODUCIBILITY.md` and `VERIFICATION.md`. Offline tests use an explicitly
scripted model and require no credential. The executed notebook makes one
new narrow live run, then clearly reads the saved eight-case suite.
Reruns may vary; no byte-identical model-answer promise is made.

`outputs/development_attempts/` retains earlier LLM behaviors for transparency,
not as the final evaluation. Superseded rule-only outputs have been removed.
`outputs/live_access_check.json` distinguishes earlier access errors from the
subsequent successful connection.

Replit AI assisted with planning, implementation, debugging, testing and writing.
Edward must review, understand and personalize the work according to course
policy. Nothing here uploads coursework or merges the draft PR.
