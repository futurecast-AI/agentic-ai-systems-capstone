# LLM-powered agentic workflows capstone — revision

**AI Foundations (Edward Hickman) · Udacity · Project 6**

> **Not ready to resubmit yet.** The LLM architecture has been implemented and
> offline-tested. The replacement MiniMax key is rejected with HTTP 401 at
> both documented global and mainland-China endpoints. Earlier checks returned
> OpenAI `insufficient_quota` (429) and, with the previous MiniMax key,
> `insufficient_balance_error` (402). Authentication must be resolved before
> making any new credit diagnosis. No successful live response is claimed. The current
> `module_summary.*`, notebook and `outputs/runs/` still describe the rejected
> rule-based version and must be rebuilt, not uploaded as the revision.

## What changed

The original implementation incorrectly treated a predefined Python checklist as
sufficient. The reviewer requires actual LLM-directed planning. The new
`agentic_system.py` uses **LangGraph** and LangChain **ChatOpenAI**:

`user instructions → LLM decision → guarded read-only tool → observation → LLM decision`

The LLM chooses which tool to call and when to answer. The controller does not
contain a predefined sequence or a keyword-to-tool planner. A missingness-only
request and a duplicate-only request can require different plans. Application
guards enforce dependencies, capabilities and budgets; they do not pick the
next analytical check.

## Identifiable agent components

- **Persona:** cautious data-quality reviewer, defined in `PERSONA`.
- **Reasoning/decisions:** model-selected function calls with brief public action
  justifications; observations are returned before the next decision.
- **Tools:** load, profile, missingness, duplicates, numeric validity, categories.
- **Memory:** fresh LangGraph message history, observations, working frame, trace,
  completed tools and counters per run. No persistent cross-run memory.
- **Boundaries:** read-only registered public data, six tool calls, eight model
  turns, no arbitrary paths, writes or shell tools. Calls have a provider timeout;
  this is not a universal end-to-end or process-isolation guarantee.

Public action summaries are not private chain-of-thought. The MiniMax M3 client
disables its optional thinking output; the LLM still selects actions from
instructions and observations. Do not claim biological validity from the narrow
numeric rules or trust generated explanations without checking observations.

## Setup and credentials

Tested locally with Python 3.11.18. The dependency freeze includes the actual
installed LangGraph/LangChain/OpenAI packages and scientific/notebook libraries.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Supply `MINIMAX_API_KEY` through your environment or secure Secrets manager.
The default is **MiniMax-M3** at `https://api.minimax.io/v1`.
Provider configuration is in `config.json`.

To use funded OpenAI instead, supply `OPENAI_API_KEY` and set
`AGENT_LLM_PROVIDER=openai`; its configured model is `gpt-4.1-mini`.
The two keys are never substituted for one another or sent to each other's
endpoint. Provider switching is explicit, not a hidden fallback.

No key belongs in code, notebooks, logs, `.env` commits or the submission.
API usage may cost money. A key's existence does not establish quota.

## Run the implementation

After usable provider credit is available:

```bash
python agentic_system.py
python evaluate_agent.py
```

The evaluation runner uses actual provider calls and saves observations,
selected actions, final answers and usage metadata in `outputs/llm_runs/`.
It never silently replaces a failed request with scripted responses.
The existing files in that directory are **failed OpenAI attempts**, not
successful planning evidence. The separate `outputs/live_access_check.json`
records the sanitized provider blockers.

## Offline verification

```bash
python -m pytest tests -q
```

Tests use explicitly scripted model responses to check the real LangGraph loop,
observation feedback, alternative action orders, validation, dependency/budget
guards, refusal, error handling, state isolation and unchanged data.
**These are software unit tests, not live-model evaluation.**

## Remaining work before upload

Run and inspect real LLM cases, including distinct natural-language tasks and
an observed limitation/failure. Then replace the old notebook, report, scenario
outputs and documentation with evidence from those runs; regenerate and verify
the submission ZIP. See `SUBMISSION_CHECKLIST.md` and `RESUBMISSION_STATUS.md`.

AI assistance was used for design, implementation, tests and drafting.
Edward must understand and personalize the work according to course policy.
Nothing here automatically submits coursework, merges the PR or establishes
reviewer acceptance.

## Five-sentence implementation summary

This single LLM-powered reviewer uses LangGraph to alternate model decisions
with read-only dataset tools and run-local message memory.
The model interprets natural-language requests and chooses its next tool or
final response after receiving observations.
Application guards enforce allowlists, dependencies and budgets without
supplying a fixed sequence of checks.
Offline tests exercise control and safety using scripted responses, but live
provider evaluation is currently blocked by insufficient credit.
The implementation cannot certify scientific data validity or replace human
judgment, and it is not yet a completed resubmission.
