# Improvement Changelog

This file starts **before** model experiments so we preserve the real development story.

| Stage | Hypothesis/change | Evidence | Decision |
|---|---|---|---|
| v0 | Separate natural-language interpretation from formal feasibility proof. Freeze benchmark before model tuning. | 12 synthetic gold cases + solver sanity check | IN PROGRESS |
| v0.1 | Add a strict constraint schema and validator between AI extraction and the formal solver. | Case 02 gold constraints accepted; unsupported `probably_delayed` output rejected; duplicate IDs rejected; automated suite passes 7/7 tests. | KEEP |
Do not backfill fictional improvements. Add a row only after running and saving an experiment.
