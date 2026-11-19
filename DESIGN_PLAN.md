# Bounded data-quality review agent — design before implementation

Single-agent, deterministic Python sense/decide/act workflow. It is a rule-based
agent with limited autonomy, not an LLM or a general reasoning system.
The assignment explicitly accepts reasoning **or decision logic** and optional
LLM use; no API, new agent framework or credentials are required.

Persona: cautious data-quality reviewer. Goal: inspect one registered public
Palmer Penguins CSV, choose applicable checks and return evidence for a human.
New task, data and workflow: no agent or dataset is reused from earlier capstones.

Tools: load an allowlisted local dataset, profile schema, count missing values,
check repeated rows, validate numeric measurement representation and positivity,
check known categorical values. All tools are read-only. Dataset strings are data,
not executable instructions. No arbitrary paths, network, shell, eval, SQL,
deletions, imputation, file edits or external messages exist in the agent.
The evaluation harness, not the agent, writes outputs and creates test fixtures.

Limited state: per-run observations, completed-tool names, bounded event trace,
call count and terminal status; working DataFrame remains in local run memory.
No cross-run memory or raw-row logging. Reset state for every request.

Decision loop: validate request → load → profile → missingness → duplicates →
numeric checks if expected measurement columns exist → category checks if expected
categorical columns exist → finish. Record conditional skips; stop on any tool
failure or exhausted call budget. Maximum six tool invocations. Use short
explicit policy reasons, not hidden chain-of-thought.

Safeguards: allowlist only `penguins`, intent only `review`, size <=1 MB,
rows <=5,000, columns <=20, verify original source SHA-256, bounded dispatch,
missing checks never called “passed,” no data changes, aggregate logging,
human-review disposition if findings exist. A checks-clear result means only
that configured checks found nothing; never certify all data quality.

Evaluation cases fixed before implementation:

1. Unmodified source: complete, missing data sent for human review.
2. Complete-case subset (explicit fixture): complete, configured checks clear.
3. Append duplicate row (explicit fixture): complete, duplicate flagged.
4. Negative body mass (explicit fixture): complete, numeric issue flagged.
5. Categories-only subset: complete, numeric check skipped, schema held for review.
6. Unsupported dataset/path request: blocked before any tool.
7. Request to delete rows: blocked before any tool.
8. Small tool budget: incomplete, never asserted clean.
9. Injected numeric-tool failure: failed, subsequent tools not run.
10. Empty frame fixture: failed safely after bounded calls.
11. Instruction-like category string: treated as data; category issue flagged.
12. Positive but absurd mass: demonstrates known limitation—positivity checks miss
    scientifically implausible values. Do not hide it or change policy to pass.

Fixtures are transparent deterministic alterations of the public data solely
for exercising branches; they are not presented as real field observations.
No production accuracy or broad robustness claim from this small designed suite.
Provide actual traces, independent assertions, architecture diagram, a finalized
notebook with 4–6 sentence ending summary, cited APA report and actual pip freeze.
