# Retained development evidence — not the current evaluation

- `multiple_tool_requests.json`: the first live full-review attempt, before
  batch-rejection feedback existed. It loaded/profiled the CSV, then requested
  missingness and duplicates together. The guard executed neither and stopped.
  The implementation at that stage is in commit
  `b5d6d348ecb3686cdcdf5a36f3218011418e03a6` (before the live revision changes).
- `first_completed_suite/`: the eight-case live suite after adding batch feedback,
  but before strengthening instructions about evidence grounding and refusing
  unsupported edits. Its manifest records that stage's code hash, configuration
  and persona. It includes problematic model interpretations, not validated
  answers.

These are selected retained development records, not an exhaustive record of
all preparation requests or a held-out test set. The current eight-case results
are in `outputs/llm_runs/`; final prose limitations are in
`outputs/explanation_audit.json`. No saved model answers were edited to make
them look correct.
