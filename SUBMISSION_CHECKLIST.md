# Revised submission checklist — not ready for upload

## Implemented

- [x] Real LLM client integrated with LangGraph; not an unused API wrapper.
- [x] Natural-language instructions enter the model context.
- [x] Model-selected tools; no predefined analytical checking sequence.
- [x] Tool observations return to the LLM before its next action.
- [x] Persona, message memory, working state and action trace are identifiable.
- [x] Read-only capabilities, validation, dependency and budget guards.
- [x] Separate MiniMax/OpenAI configuration and secret names.
- [x] Offline tests clearly distinguished from live-provider behavior.

## Required before revised submission

- [ ] Usable provider credit and an actual successful LLM response.
- [ ] Saved real multi-step model/tool/observation/final-answer traces.
- [ ] Different natural-language tasks with observed selected plans.
- [ ] Real failure/limitation analysis, without forced-success claims.
- [ ] Updated executed `agentic_system.ipynb`; no stale rule-based narrative.
- [ ] Updated `module_summary.pdf`, all required sections and in-text citations;
      at least two credible sources, including one scholarly source.
- [ ] Revised architecture diagram matching the LLM implementation.
- [ ] Final actual `pip freeze > requirements.txt`, installation and rerun checks.
- [ ] Verified secret-free ZIP containing the revised, consistent artifacts.
- [ ] Edward's personal review/understanding and course AI-policy check.

The prior PDF/notebook/output bundle is the rejected version, not a fallback
acceptable submission. Do not label the failed API requests as LLM execution.
