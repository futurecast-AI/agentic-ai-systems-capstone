# An LLM-Directed Data-Quality Review Agent

AI Foundations (Edward Hickman)

## Overview

This resubmission replaces the rejected deterministic controller with an actual LLM-directed agent built using LangGraph, LangChain and MiniMax-M3. It reviews one registered public Palmer Penguins CSV and explains evidence to a person. The model interprets natural-language instructions, selects tools and decides what to do after each observation. Python enforces capability boundaries but does not prescribe the analysis sequence. The contribution is a bounded demonstration of model-directed review, not autonomous data cleaning, production readiness or scientific certification.

## System Architecture and Design

The persona is a cautious data-quality reviewer: inspect, explain and leave changes to a human. One agent is sufficient because the task uses a shared evidence state and no independent specialist roles. Its LangGraph StateGraph alternates llm_decision and read_only_tool nodes. LangGraph distinguishes predetermined workflows from agents whose tool use is dynamic (LangChain, n.d.). A fixed graph does not imply a fixed tool plan: the model chooses the action identity, relevance, order and final response.

Six tool schemas expose load, profile, missing, duplicates, numeric and categories. LangChain's ChatOpenAI binds them to MiniMax's OpenAI-compatible endpoint (MiniMax, n.d.). Actual evaluation used MiniMax-M3; an explicitly selected OpenAI configuration exists but was not the successful provider. Keys are environment-only and absent from the submission. Optional model thinking output is disabled. Brief public action justifications and tool observations are recorded, not private chain-of-thought.

Each run has fresh message history, aggregate observations, completed tools, counters, trace and a temporary DataFrame. The model receives messages; only tools access the frame. There is no persistent memory or cross-run learning. The source has 344 rows and eight columns, distributed by Horst et al. (2020) from Gorman/Palmer Station LTER data. Its CC0 attribution, original bytes and SHA-256 are included. Figure 1 shows this implemented architecture.

## Decision Logic and Behavior

The user supplies a natural-language instruction inside a validated Request. The LLM requests a tool with a public reason. After validation, Python executes that requested tool and returns its aggregate result as a ToolMessage. The LLM sees the accumulated history and chooses another action or finishes. This action/observation cycle is inspired by ReAct (Yao et al., 2023), not a reproduction of its tasks, prompts or reported benchmark gains.

Loading must precede data checks; numeric and categories require a profile. These are tool preconditions, not a Python scheduler selecting which check comes next. Unknown tools, malformed arguments, repeated tools and violated dependencies stop safely. An early real model request contained two tools despite the single-call setting. The initial guard blocked it. The revised guard executes neither, returns rejection observations and lets the model choose one action itself. Model-turn limits also bound repeated rejections.

The result wrapper independently reports full configured coverage, findings and disposition. A narrow completed task is partial_review, not a full quality certificate. Tool failures return an observation that the model can explain; further tools are unavailable after a fault. The model is not allowed to invent missing evidence or silently substitute a review when the user asks for an unsupported edit.

## Safety, Reliability, and Transparency

The registered source and tool names are allowlisted. Input and tool arguments are validated; source loading checks byte/shape limits, column labels and fingerprint. There are at most six tool executions and twelve model turns, including format-repair turns. The client has a sixty-second timeout setting and no automatic provider retries. These are not an end-to-end runtime or monetary guarantee. The tools cannot edit data, run shell commands or send messages; the separate evaluation harness writes the JSON/CSV artifacts.

Logs preserve model-selected calls, public reasons, observations, response identifiers, usage and final answers. They are evidence of observable behavior, not faithful access to internal reasoning. Raw cell strings are not forwarded by these tools, but user instructions and aggregates reach a third-party API. Transparency, bounded authority and human accountability are risk controls consistent with NIST (2023), not certification. There is no OS isolation, general injection defense or automatic recovery from arbitrary programming errors.

## Observed Behavior and Limitations

Eight current designed cases have saved real provider transcripts. The original-data run returned completed/human_review, using 6 tool executions and 7 model turns. It found 19 missing cells across 11 records, with zero full-row repeats and zero violations of the configured numeric/category rules. Missingness-only used load → missing; duplicates-only used load → duplicates. These distinct paths were selected from different user instructions, not Python keyword branches. The appendix records every current case.

The two-call case ended budget_exhausted with 2 executions. The injected numeric fault ended failed; its error observation returned to the model for an explanation. The deletion-request trace documents the actual response; no editing capability exists and the source fingerprint stayed unchanged. The reduced-column fixture is a declared projection, not discovered corruption or proof of repeated animals.

The 333-row complete-case fixture with 999,999 g still returns configured_checks_clear. The numeric tool checks only finite, positive representations and exposes no actual mass. Adding an LLM cannot reveal information its tools never return. Early retained development responses also inferred row-level overlap and overinterpreted attribute repeats. Instructions were strengthened and final responses were inspected without editing their saved prose. The final original-data explanation still contains errors: it calls 11 roughly three times 2 (the ratio is 5.5), and its bottom line treats other variables as complete despite four reported measurement gaps of two each. The reduced-schema answer initially says three absent columns before correcting itself to five. These are retained narrative errors, not tool-count errors; prompt changes improved some responses but did not establish reliable explanations.

The current suite is small, purpose-built and used during development, not an untouched reliability benchmark. Offline tests use a scripted model and check software properties; they are separate from live LLM evidence. There is no random task sample, multi-run success estimate, baseline comparison, confidence interval or independent user study.

## Interpretation for a Non-Technical Audience

A language model reads the request and chooses from a small set of checking tools. After each result, it decides whether another check is needed. For the full penguin table, the tools found 19 blank entries spread across 11 records. A person receives the findings; nothing is deleted or filled in. A request just about blanks leads to fewer checks than a full review. The program stops if its allowance runs out or a checking function fails. It can still miss serious problems: a test weight of 999,999 grams passed because the available rule checked only that it was a positive number. The model's written explanation can also go beyond what the checks establish. A person must inspect the evidence before making changes.

## Ethical and Responsible Use Considerations

A fluent explanation can create overtrust. A completed run or configured_checks_clear does not mean the data are scientifically correct. The known mass miss and explanation errors make that boundary concrete. Structured counts remain visible beside model prose, and human review—not automatic cleaning—retains authority (NIST, 2023).

Deleting missing or repeated-attribute records could distort representation. The agent cannot decide that such rows identify the same animal or should be discarded. Public animal data reduce some privacy risks but do not establish safety for private human records; provider disclosure, access, consent and retention would need review. No fairness or ecological-bias assessment was performed.

Replit AI assisted with planning, implementation, debugging, testing and drafting. Edward must review, understand and personalize the work under course policy. Saved provider responses are unedited evidence; constructed fixtures are labeled. Reproducible software assertions do not establish independent authorship, production safety or a passing classroom decision.

## Future Improvements

First, define domain-expert measurement ranges and cross-field checks, then evaluate them on new cases rather than retroactively declaring the known miss detected. Supply evidence sufficient for row-overlap questions instead of inviting the model to infer it from marginals. Test explanation grounding with independently annotated questions and repeated runs across models; report abstention and error rates separately from tool completion. More prompts alone are not a reliability proof.

A deployed version would also require process isolation, end-to-end timeouts, access controls, protected audit retention, explicit provider cost limits and human approval before any future write capability. Keep these proposed controls separate from the implemented safeguards. No production deployment, automatic repair or broader dataset competence is claimed by this resubmission.

## References

Horst, A. M., Hill, A. P., & Gorman, K. B. (2020). palmerpenguins: Palmer Archipelago (Antarctica) penguin data [Data set]. https://doi.org/10.5281/zenodo.3960218

LangChain. (n.d.). Workflows and agents. https://docs.langchain.com/oss/python/langgraph/workflows-agents

MiniMax. (n.d.). OpenAI API compatibility. https://platform.minimax.io/docs/api-reference/text-openai-api

National Institute of Standards and Technology. (2023). Artificial intelligence risk management framework (AI RMF 1.0). https://doi.org/10.6028/NIST.AI.100-1

Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. International Conference on Learning Representations. https://openreview.net/forum?id=WE_vluYUL-X
