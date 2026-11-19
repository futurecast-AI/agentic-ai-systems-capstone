# A Bounded Data-Quality Review Agent: Design, Behavior and Safeguards

AI Foundations (Edward Hickman)

## Overview

This project implements a single bounded, rule-based data-quality review agent for a registered public Palmer Penguins CSV. It observes data, chooses applicable read-only checking tools, remembers results within a run and returns an aggregate report for a human. It has explicit decision logic rather than an LLM, free-form planning or API dependence. The aim is transparent small-scale workflow design, not autonomous data repair or production certification.

## System Architecture and Design

The agent's persona is a cautious reviewer: inspect, explain and defer changes to a human. An agent architecture organizes decisions and actions in relation to an environment; that concept is broader than LLM-based systems (Wooldridge & Jennings, 1995). Here the environment is deliberately small: a single registered local CSV and six allowlisted Python tools. This is a constrained sense/decide/act workflow, not a claim of general intelligence or the full range of agent properties discussed in that literature. One agent is sufficient because the task has a shared observation state and no independent roles needing coordination.

Figure 1 shows the actual components and interactions: a structured Request, input gate, rule-based decision loop, per-run RunState, tool dispatcher and terminal report. RunState stores completed and skipped tool names, aggregate observations, a call counter, ordered trace and temporary working DataFrame. Every request starts with a fresh state; there is no persistent memory, conversation history or learning across runs. Short policy reasons in the event trace expose decisions, not a model's private chain of thought.

The six tools load the registered CSV, profile its schema, count missing values, count repeated rows, validate numeric measurements and check categorical membership. The source contains 344 penguins and eight columns, distributed in palmerpenguins by Horst et al. (2020), with data collected by Kristen Gorman and Palmer Station LTER. The 15,241-byte CSV is included unchanged with a pinned repository revision, SHA-256 and CC0 attribution notice. This dataset and agent are new to the capstone sequence. The workflow does not train a predictor, infer ecological relationships or reuse a prior capstone's agent.

## Decision Logic and Behavior

The public entry point accepts only dataset ID penguins, intent review and an integer tool budget from one to six. Any unsupported request terminates before a tool is called. The default run selects load, then profile, missingness and duplicates; numeric and categorical checks are selected only when the observed profile contains applicable columns. Completed-tool memory prevents repeat calls and records skipped checks. This is coded policy selection, not natural-language understanding or LLM-generated tool choice.

The original-data run completes the six tools and records thirteen trace events. Numeric validation checks the four measurement columns for nonmissing values that are nonnumeric, nonfinite or nonpositive. Category checks compare species, island and sex with the configured vocabularies. Missingness uses pandas isna(), avoiding incorrect equality comparisons with NaN (pandas development team, n.d.). Year content, scientific plausibility, record identity and cross-field relationships are outside the implemented rules.

The categories-only fixture demonstrates conditional selection: no measurement columns are present, so numeric validation is explicitly skipped and the run uses five calls. The reduced schema is flagged for human review. If a tool fails, execution stops without retry or claims about unperformed checks. If the next required call exceeds the budget, the terminal status is budget_exhausted. Completed status means applicable configured checks finished; disposition separately identifies human review, configured checks clear, or incomplete review.

## Safety, Reliability, and Transparency

Safeguards are implemented capabilities and limits, not statements that the system is generally safe. The agent cannot select arbitrary paths or tools: only the registered dataset and six dispatcher names are accepted. Original-source loading checks a one-megabyte byte limit and SHA-256, then rejects empty or over-5,000-row frames, more than twenty columns, repeated column labels or invalid labels. The bounded loop has at most six tool calls and no retry cycle. Expected I/O, parsing and tool errors stop the run and return incomplete review. No data-editing, network, shell or message-sending tool exists.

Returned traces contain action names, short fixed reasons and outcomes; observations contain aggregates rather than raw row contents. The evaluation harness writes JSON and CSV results and builds altered fixtures, while the agent itself neither writes reports to disk nor changes the source. Request validation, bounded action space, evidence logging and human control are risk-management design choices aligned with transparency and accountability principles, not NIST certification (National Institute of Standards and Technology [NIST], 2023).

An instruction-like species value is treated only as an unexpected category; it is not executed or forwarded to an LLM. This is a narrow control/data separation test, not evidence of general prompt-injection resistance. Configurations and local Python code are trusted inputs. There is no OS-level isolation, cancellation of a hung function, wall-clock timeout, arbitrary-bug recovery or broad adversarial test. Aggregate logging is not a privacy guarantee for sensitive future data.

## Observed Behavior and Limitations

Twelve scenarios specified before implementation were actually run. The original 344-row dataset contains 19 missing cells across 11 records: two missing entries in each of four measurements and eleven in sex. The agent returns human_review, with zero repeated full rows and zero violations of the configured numeric or categorical rules. Source hashes before and after the suite are identical. The agent does not decide why values are absent or silently delete them.

The complete-case fixture contains 333 rows and returns configured_checks_clear. The duplicate fixture flags one appended repeat; the negative-mass fixture flags one invalid measurement. The categories-only fixture skips numeric validation but counts 331 repeats among its three retained attributes. These are shared attribute combinations, not proof of repeated animals: the example exposes the importance of human interpretation before removal.

An unregistered path request and a delete-row request are both blocked with zero tool calls. A two-call budget stops after load and profile. The injected numeric-tool failure uses five attempted calls, stops before categories and returns failed/incomplete_review; this is a simulated fault, not a pandas outage observed in the base run. An empty-frame fixture fails at loading. The instruction-text fixture flags one unexpected species value without executing the text.

The most important known miss is the complete-case fixture with a 999,999 g body mass. It still returns configured_checks_clear because the rule checks only positivity, finiteness and numeric representation. This exposes limited domain knowledge; it is not evidence that such a mass is acceptable. All twelve predeclared policy expectations are observed, including that miss. This is not a 100% anomaly-detection rate, broad reliability estimate or safety guarantee. The small purpose-built suite has no random task sample, confidence interval, baseline comparison or independent user study.

## Interpretation for a Non-Technical Audience

The program checks a table of penguin records and tells a person what needs attention; it does not change the table. In the original table, it found 19 blank entries spread across 11 records and asked for human review. It refused a request to delete records and stopped when a test checking function was made to fail. It can still miss important problems: a test weight of 999,999 grams was not flagged because the program only checked that weights were numbers greater than zero. A person must therefore check what the warnings mean and decide what, if anything, to change. Finishing these checks does not prove that every value in the table is correct.

## Ethical and Responsible Use Considerations

The main autonomy risk is overtrust: a researcher could treat completed or configured_checks_clear as permission to publish or use data without further review. The 999,999 g miss shows why that would be unjustified. The implemented response includes a narrow scope warning, keeps completion separate from disposition and offers no automatic repair. A human remains accountable for interpreting findings and making changes, consistent with contextual risk-management responsibilities (NIST, 2023).

Automatic removal could also change which groups are represented. Eleven missing sex entries do not by themselves justify deleting those animals, and repeated species/island/sex combinations do not establish duplicate records. This agent flags aggregate issues instead of inventing values or deciding whose records to discard. It does not measure demographic fairness, ecological selection bias or impacts of any proposed cleaning policy. The public animal dataset is low-sensitivity; applying the design to private human records would require additional access, retention and privacy analysis.

Transparency also requires honest naming. This is a rule-based semi-autonomous reviewer, not an LLM assistant with human-like reasoning. The logs record coded policy reasons, not explanations recovered from a learned model. AI assistance was used for implementation, testing and drafting; Edward must review, understand and personalize the work according to course policy. Reported behavior comes from the included executions. Test alterations are labeled as fixtures, not presented as defects discovered in the real field observations.

## Future Improvements

First, collaborate with a domain expert to define scientifically justified measurement ranges and year/cross-field rules, then test them on held-out cases rather than retroactively claiming the known miss was detected. Add schema-specific identifiers before treating repeated rows as duplicate entities. Expand evaluation to additional registered datasets and independent task cases, while preserving clear completion and uncertainty reporting.

A deployment-oriented version would need process isolation, timeouts, access controls, protected audit storage and an explicit approval mechanism before any future write capability. These are not implemented or validated here. An LLM could eventually help interpret user requests, but would add nondeterminism, costs and untrusted-instruction risks; it would still need the same restricted dispatcher and stronger evaluation. No such extension is claimed as completed work.

## References

Horst, A. M., Hill, A. P., & Gorman, K. B. (2020). palmerpenguins: Palmer Archipelago (Antarctica) penguin data [Data set]. https://doi.org/10.5281/zenodo.3960218

National Institute of Standards and Technology. (2023). Artificial intelligence risk management framework (AI RMF 1.0) (NIST AI 100-1). https://doi.org/10.6028/NIST.AI.100-1

pandas development team. (n.d.). Working with missing data. https://pandas.pydata.org/docs/user_guide/missing_data.html

Wooldridge, M., & Jennings, N. R. (1995). Intelligent agents: Theory and practice. The Knowledge Engineering Review, 10(2), 115–152. https://doi.org/10.1017/S0269888900008122
