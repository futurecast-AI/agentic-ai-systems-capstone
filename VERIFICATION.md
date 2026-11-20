# Verification record — LLM revision, live execution blocked

## Offline checks

The revised suite exercises the actual LangGraph loop using explicitly
scripted model responses. It tests alternative selected tool sequences and
narrow requests, returned observations, fresh memory, source/fixture
immutability, allowed tools/arguments, dependency guards, model/tool budgets,
error observations, no silent retries, scoped completion and provider/key
separation. See `outputs/validation.txt` for the current executed test count.

These unit tests establish specified software behavior, not an LLM's actual
planning quality. The original source remains fingerprinted at
`f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93`.

## Provider checks

OpenAI: configured key was passed only to `api.openai.com`. The live runner's
eight attempts returned no AI message. A bounded diagnostic established HTTP 429,
type `insufficient_quota`, code `credit_balance_exhausted`.

MiniMax: configured key was passed to the documented MiniMax endpoint.
The bounded text probe returned HTTP 402, type `insufficient_balance_error`.
The documented quota endpoint returned success but zero allocated text usage.
No key values, partial values or request authorization headers are saved.

No successful live response or completed model-driven case is claimed.
Do not reuse failed requests as success evidence. Automatic repeated requests
will not repair these credit limitations.

## Pending verification and deliverables

Successful real-provider execution, updated notebook and APA report, revised
diagram, final clean-environment replay and new submission ZIP are pending.
Legacy reports, notebook outputs and `outputs/runs` belong to the rejected
rule-based architecture. They are not evidence for the new agent.

No classroom submission, reviewer pass, PR merge or CI pass is claimed.
