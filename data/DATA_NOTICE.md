# Palmer Penguins: source and attribution

Unmodified `penguins.csv`, 344 rows × 8 columns, from:
https://raw.githubusercontent.com/allisonhorst/palmerpenguins/8957207b78d6ccd1b4654a9dd9c9041b657478ab/inst/extdata/penguins.csv

Source repository revision: `8957207b78d6ccd1b4654a9dd9c9041b657478ab`
SHA-256: `f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93`
Size: 15,241 bytes.

Horst, A. M., Hill, A. P., & Gorman, K. B. (2020).
*palmerpenguins: Palmer Archipelago (Antarctica) penguin data*.
https://doi.org/10.5281/zenodo.3960218
Project documentation: https://allisonhorst.github.io/palmerpenguins/

Data were collected and made available by Kristen Gorman and Palmer Station
Antarctica LTER. The source documentation states the data are available under
CC0. Follow the linked LTER data-use guidance and credit the collectors when
using or publishing analyses. This capstone demonstrates data-quality software,
not new ecological findings.

The official CSV is included unchanged. Evaluation fixtures are explicitly
documented copies altered in memory by `evaluate_agent.py`; they do not replace
the source file and are not presented as real field measurements.

The read-only dataset tools make no network call. The revised agent's LLM
client sends the user task and aggregate tool observations to the explicitly
selected MiniMax or OpenAI endpoint, using a securely supplied provider key.
To recover a missing source file, manually download the exact pinned URL above
and check its SHA-256.
