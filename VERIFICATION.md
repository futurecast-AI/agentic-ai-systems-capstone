# Verification record

## Local checks

`python -m pytest tests -q`: **33 passed**; saved in `outputs/validation.txt`.

Checks cover original-data counts and trace order, blocked structured and
free-form requests, every supported call budget, conditional numeric-tool
skipping, fault stopping, numeric invalid values, instruction-like cell values,
fresh per-run memory, unchanged fixtures, shape guards, source-tamper detection,
unknown-tool rejection, exact scenario replay, notebook execution, required
report sections, diagram presence, five-sentence summary, jargon-free plain
explanation, actual freeze and original APA-template preservation.

The test suite retains the **known semantic miss**: 999,999 g is positive and
therefore not flagged by the narrow numeric rule. Its passing test documents
that limitation; it is not successful anomaly detection.

## Independent reproduction

Created a new Python 3.11.18 environment from `requirements.txt` and a clean
directory containing only the implementation, evaluation harness, configuration,
notebook and original CSV. No previous outputs were copied.

Ran the notebook top to bottom and compared every generated file in
`outputs/runs/` against the originals. All twelve scenario JSON files,
`source_integrity.json` and `evaluation_summary.csv` matched byte-for-byte.
The original source remains at SHA-256
`f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93`.

This verifies the documented stack, not identical results under every
possible dependency, configuration or operating system.

## Visual review

Viewed the architecture diagram and rendered all **ten report pages**.
Checked component names, reasoning flow, state, tool/observation arrows,
blocked-request path and terminal output. No clipping or missing pages found.
The plain-language section is entirely on **page 5**.

The diagram shows the implemented rule loop, not a hypothetical LLM system.
The report uses four cited credible sources, including the scholarly
Wooldridge and Jennings article, and describes only actual implemented safeguards.

## Scope and limitations

No paid API or secrets are used. The agent has no network, shell or data-edit
capability, but is not isolated in an OS security sandbox. It has no wall-clock
timeout, general planning, cross-run learning or scientific plausibility rules.
Dataset/intent allowlists and six-call ceiling are application restrictions,
not comprehensive security assurance.

No GitHub Actions workflow is configured. Local checks do not imply CI passed.
Remote head, PR state and required checks are checked separately after publication.
No classroom submission or reviewer acceptance has occurred.
