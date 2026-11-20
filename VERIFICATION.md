# Verification of the LLM-directed resubmission

## Real model behavior

`outputs/llm_runs/` contains eight current MiniMax-M3 scenario records and
35 actual provider-response turns. There is no fake fallback.
`run_manifest.json` fingerprints the implementation, evaluator and configuration.
The current source hashes match that manifest.

| Case | Actual result | Tool executions |
|---|---|---:|
| Original CSV | completed / human_review | 6 |
| Missingness only | completed / partial_review | 2 |
| Duplicates only | completed / partial_review | 2 |
| Three-column fixture | completed / human_review | 6 |
| Budget of two | budget_exhausted / incomplete_review | 2 |
| Injected numeric fault | failed / incomplete_review | 3 |
| Delete/overwrite request | completed / partial_review; refusal | 0 |
| 999,999 g fixture | completed / configured_checks_clear; known miss | 6 |

The full run used seven model turns. Missingness/duplicates requests selected
different short paths; the injected fault returned an error observation before
the model's final explanation. The model—not a Python keyword planner—selected
these actions. Full configured coverage is computed independently.

**Completed does not mean correct.** The final explanation audit retains a
ratio error, a recommendation inconsistent with the missingness table and a
self-corrected schema-count mistake. The three-column fixture also elicited an
unnecessary numeric check with an empty result. The model cannot detect the
hidden 999,999 g value through aggregate positivity-only tools.

## Offline and clean-environment checks

- **52 tests passed** in the working Python 3.11.18 environment.
- The actual `pip freeze` installed into a new Python 3.11.18 environment;
  `pip check` reported no broken requirements and **52 tests passed** there.
- The final notebook was also executed using that clean environment's explicit
  kernel. Its live missingness demo made two tool executions and three model
  turns; all nine code cells executed without error outputs.
- Unit responses are scripted by design, not live LLM evidence.
- Source compilation and whitespace checks are separate from behavioral tests.

An initial clean-setup command selected the sandbox's unrelated Python 3.14,
whose NumPy could not load its C++ runtime. That setup was not the documented
target; the explicit Python 3.11 environment installed and passed. Use the
specified interpreter, not an arbitrary `python3` alias.

## Report and browser inspection

The revised PDF has nine pages. The DOCX opens and converts successfully.
The course template's styles, section geometry and header/footer bytes were
preserved; `outputs/report_template_audit.json` records the checks.
The report's pages and architecture figure were rendered/visually inspected,
with text bounds checked for clipping. Instructor/due-date fields were not
invented.

The exported executed-notebook HTML was checked in a desktop browser. The
current eight-case table was fully visible without clipped columns, including
the two intended incomplete cases and zero-tool refusal. This browser check
read saved results; it did not execute the agent.

The served PDF is checked against the local PDF by fingerprint. Temporary
preview availability is not a substitute for the included offline files.

## Integrity and scope

The original CSV fingerprint remained unchanged. Test fixtures are declared
trusted copies; no source edit is authorized. Current provider keys are scanned
for accidental inclusion before publication/packaging; none belongs in the ZIP.
No `.env`, environment directory or Git metadata is intended for the archive.

Earlier access failures and development traces are historical evidence only.
Superseded rule-only scenario files were removed from the current submission;
the source history remains available.

Local verification is not a CI pass, independent model-quality assessment,
security certification, classroom submission or passing reviewer decision.
The PR remains draft pending Edward's review; no merge is authorized.
