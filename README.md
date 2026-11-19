# Agentic AI Systems capstone

**AI Foundations (Edward Hickman) · Udacity · Project 6**

A single rule-based data-quality reviewer with explicit decision logic,
run-local memory, six read-only tools, bounded execution and observable traces.
**No LLM, API key, external agent framework or paid service is required.**
This is a semi-autonomous function-orchestration workflow, not a natural-language
assistant. The assignment permits explicit decision logic and optional LLM use.

## Submission contents

- `agentic_system.ipynb` — executed walkthrough, complete source display, diagram,
  original-data run, twelve evaluation scenarios, findings and five-sentence summary.
- `agentic_system.py` — full runnable agent implementation; notebook uses this module.
- `module_summary.pdf` — ten-page cited APA report with all required sections,
  architecture diagram and plain-language explanation on page 5.
- `requirements.txt` — actual working-environment `python -m pip freeze`.
- `config.json`, `data/penguins.csv`, `data/DATA_NOTICE.md` — required configuration
  and unmodified public CC0 source with pinned URL, hash and attribution.
- `evaluate_agent.py` and `outputs/runs/` — explicit fixture setup and actual
  aggregate outputs, decisions and traces for every scenario.
- `outputs/architecture_diagram.png` — separate architecture diagram.

The editable Word report, Markdown report, HTML notebook export, design plan,
tests, verification notes and submission checklist are also included.

## Run from the repository root

Tested on Python **3.11.18 / Linux**:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python agentic_system.py
python evaluate_agent.py
python -m pytest tests -q
```

`agentic_system.py` prints a complete original-data result and performs no disk
writes. `evaluate_agent.py` explicitly writes the twelve scenario results to
`outputs/runs/`. All runtime source data are bundled; the agent uses no network.
The file fingerprint must match the pinned original. Configuration and local
code are trusted inputs, not a security boundary against a malicious developer.

To use the notebook:

```bash
python -m jupyter notebook
```

Open `agentic_system.ipynb`, restart the kernel and run all cells. Keep the script,
configuration and data folders beside the notebook. Noninteractive alternative:

```bash
python -m nbconvert --to notebook --execute --inplace agentic_system.ipynb \
  --ExecutePreprocessor.timeout=180
```

To intentionally regenerate notebook source and its HTML export:

```bash
python scripts/build_notebook.py
python -m nbconvert --to notebook --execute --inplace agentic_system.ipynb
python -m nbconvert --to html agentic_system.ipynb --output-dir outputs \
  --output agentic_system.html
```

## Actual results, not universal assurance

The original CSV has **344 rows and 8 columns**. The agent identifies **19
missing cells across 11 records**, completes six tool calls and returns
`human_review`. No full-row repeats or configured measurement/category violations
were found. It does not change the source data.

All twelve predeclared **policy expectations** are observed, including blocked
requests, budget exhaustion, conditional tool skipping, an injected tool failure
and a known miss: a complete-case fixture with **999,999 g body mass** still
returns `configured_checks_clear`, because positivity is not biological
plausibility. This is **not 100% anomaly detection or a quality certificate**.
Fixtures are declared test alterations of copies, not real field observations.

**33 local tests passed.** A fresh environment installed from the freeze and
reran the notebook, reproducing every saved scenario JSON and CSV byte-for-byte.
Original CSV fingerprints before and after the suite are identical.
See `VERIFICATION.md` for scope and limitations.

## Report and academic integrity

The report uses the previously supplied course template:
https://docs.google.com/document/d/1cv_MjQVKnGc9sbaYiOUna2155jMEvUxACwyDax-XYWI/edit

To rebuild it, additionally install LibreOffice and suitable fonts:

```bash
python scripts/build_report.py /path/to/course-apa-template.docx
```

Opening the included PDF/DOCX requires none of the report-builder setup.
Template styles, geometry and headers are retained; Liberation Sans substitutes
for Arial in the PDF. Instructor and due date were not supplied and are omitted.

AI assistance was used for implementation, tests and drafting. Edward must
review, understand and personalize the work according to course policy.
Nothing automatically submits to Udacity, marks the draft ready or merges it.

## Script summary

This single rule-based agent reviews a registered public penguin dataset with
read-only tools, a bounded decision loop and per-run state.
On the original data it completes six tool calls and sends missing-value findings
for human review without changing a record.
Designed evaluation cases exercise conditional tool skipping, duplicate and
invalid-value flags, blocked requests, budget exhaustion and a simulated tool failure.
A positive but absurd body mass exposes a deliberate limitation of the positivity-only
measurement rule rather than demonstrating scientific validation.
The workflow has no LLM, general-language planning or persistent memory and cannot
certify data quality, infer causality or replace a domain expert.
