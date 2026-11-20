# LLM-powered review agent — reviewer remediation plan

## Why the architecture changed

The November 19 submission was unable to be reviewed because its Python
conditions chose a predefined tool sequence. That rule-only design did not meet
the reviewer's requirement for an actual LLM agent. This revision replaces that
controller; renaming the old workflow or adding an unused model client is not a fix.

## Persona, goal and authority

One cautious data-quality reviewer interprets a natural-language instruction about
the registered public Palmer Penguins CSV. It chooses relevant read-only checks
and explains evidence to a human. A single agent suffices for this bounded task;
multi-agent delegation would add coordination without demonstrated benefit.
The public data and task remain distinct from earlier course capstones.

## Implemented architecture

LangGraph alternates `llm_decision` with `read_only_tool`. LangChain's
`ChatOpenAI` binds six tool schemas to the configured model (default MiniMax-M3,
with explicitly selectable OpenAI gpt-4.1-mini).
The LLM receives the user task, selects a tool and supplies a short public action
justification. Its ToolMessage observation returns to the same model context.
The model then chooses another tool or a final answer. The application supplies
no ordered list of checks and does not select missingness/duplicates/categories
from Python keyword conditions.

The only conditional routing determines whether the LLM requested a tool or
finished. Preconditions and limits are safety enforcement, not task planning.
Loading precedes data use; numeric/categories require profile evidence.
Tool failure becomes an observation the LLM can explain; no further tools run
after failure. Invalid names/arguments, repeated calls or excess budgets stop
without substituting a scripted fallback.

A real development run requested multiple tools despite the provider setting.
The revised guard executes none, returns rejection ToolMessages for the requested
calls and lets the LLM choose one itself. No replacement action is scheduled by
Python. Repeated rejections remain bounded by the model-turn ceiling.

## Memory and transparency

Each run gets fresh LangGraph message state, observations, completed tools,
working DataFrame, tool/model counters and a trace. There is no cross-run
persistent memory. Logged model action summaries and final explanations are
public outputs, not hidden chain-of-thought or proof of faithful internal reasoning.
Only aggregate results go to the provider; raw dataset cell strings do not.

## Safeguards and residual risks

Allowlisted dataset/tools, parameter validation, six tool calls, twelve model
turns, sixty-second per-request provider timeout, zero automatic provider retries, source hash,
size bounds and no edit/shell tools constrain execution. Partial evidence cannot
be labeled a full configured review by the result wrapper, even if the model
finishes early. Model narratives remain fallible and need human checking.

The model uses a network API; the read-only dataset tools do not. Provider costs,
data disclosure, service failures, nondeterminism and prompt injection remain
relevant. There is no OS isolation, end-to-end runtime guarantee, certified
security or scientific validity. Positivity-only numeric rules can still miss
an absurd positive mass; adding an LLM does not make unavailable evidence visible.

## Verification and observed limitations

Offline tests use explicitly scripted model responses to test control and safety.
They are not evidence of an LLM planning successfully. The live evaluation script
uses only real provider responses and saves different natural-language requests,
model-selected tool paths, observations and final answers to `outputs/llm_runs`.
The revised report and executed notebook use eight current real-provider cases.
Early development traces are separately retained. Final model prose still has
arithmetic and coverage errors, documented in `outputs/explanation_audit.json`.
Prompt changes did not establish reliable explanations or a held-out success rate.
Superseded rule-only results are not current evidence.
