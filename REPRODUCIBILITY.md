# Reproduce the LLM agent or inspect its evidence

## No-key inspection

Open `module_summary.pdf`, `agentic_system.ipynb` or
`outputs/agentic_system.html`. Saved outputs are included; viewing them does not
call a provider. `outputs/llm_runs/run_manifest.json` fingerprints the evaluated
implementation, evaluator and configuration. Development attempts are separate.

## Install and test

Use Python 3.11 (prepared with 3.11.18), create a virtual environment and install:

```bash
python -m pip install -r requirements.txt
python -m pip check
python -m pytest tests -q
```

These offline tests intentionally inject scripted AIMessage objects. They test
software guards, state and observation feedback, not the quality of an LLM.

## Real provider execution

Configure `MINIMAX_API_KEY` securely for an active/funded MiniMax text-API account.
Do not edit a credential into any file. MiniMax-M3 is configured through the
OpenAI-compatible endpoint; the OpenAI Python SDK name does not mean calls go
to OpenAI. Explicit OpenAI selection is documented in README.

```bash
python agentic_system.py
python evaluate_agent.py
python -m nbconvert --execute --to notebook --inplace agentic_system.ipynb \
  --ExecutePreprocessor.timeout=600
python -m nbconvert --to html agentic_system.ipynb --output-dir outputs
```

Ensure the notebook's Python 3 kernel belongs to the environment containing
the installed requirements and inherits the securely configured key.
The suite overwrites `outputs/llm_runs`; archive results first if needed.
The notebook makes one separate narrow live run, then reads the saved suite.
Model answers may differ; no exact-response or total-success guarantee applies.
Provider failures are recorded, never silently replaced by fake responses.

## Report and image

```bash
python scripts/build_diagram.py
python scripts/build_notebook.py
python scripts/build_report.py /path/to/the-course-APA-template.docx
```

The report builder requires the provided course APA template and LibreOffice.
`outputs/report_template_audit.json` identifies its source and confirms retained
styles, page geometry and headers. The template itself is not redistributed.
`build_notebook.py` creates unexecuted cells: execute them afterward to restore
genuine notebook outputs. Do not call an unexecuted rebuild “executed.”

## Limits of reproducibility

The public dataset fingerprint is checked; test fixtures are separately labeled
trusted copies. Source hashes and package freezes aid reconstruction but do not
prove scientific validity, provider stability, prompt-injection resistance,
privacy, fairness or truthful generated prose. There is no local model weight
file, external training step or automatic classroom submission.
