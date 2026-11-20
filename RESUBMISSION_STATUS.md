# Resubmission in preparation — not ready to upload

The reviewer correctly rejected the deterministic controller. The implementation
now contains a real LangGraph / ChatOpenAI tool loop, free-form instructions,
message memory, LLM-selected actions and bounded read-only tool execution.

The revised offline validation run passed **50 tests**, including provider
configuration and key-separation checks. The result is recorded in
`outputs/validation.txt`. These use scripted responses and are NOT live LLM evaluation.

Both keys have been securely configured. OpenAI rejected a real request with
HTTP 429 (`insufficient_quota`); MiniMax rejected a real request with HTTP 402
(`insufficient_balance_error`). MiniMax's quota endpoint reported zero allocated
text usage. Neither provider supplied successful model evidence.

**Pending:** usable API credit with either provider, real model runs, the revised
executed notebook, updated cited APA report and architecture diagram, final
environment freeze, updated documentation, PR update and a newly verified ZIP.
The old report/notebook and `outputs/runs/` describe the rejected rule-based
architecture and must not be used as the revised submission.

The full live runner is `evaluate_agent.py`; it saves to `outputs/llm_runs/`,
separate from legacy results. No course submission or pass is claimed.
