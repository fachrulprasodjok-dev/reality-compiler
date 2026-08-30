# Improvement Changelog

This file starts **before** model experiments so we preserve the real development story.

| Stage | Hypothesis/change | Evidence | Decision |
|---|---|---|---|
| v0 | Separate natural-language interpretation from formal feasibility proof. Freeze benchmark before model tuning. | 12 synthetic gold cases + solver sanity check | IN PROGRESS |
| v0.1 | Add a strict constraint schema and validator between AI extraction and the formal solver. | Case 02 gold constraints accepted; unsupported `probably_delayed` output rejected; duplicate IDs rejected; automated suite passes 7/7 tests. | KEEP |
| v0.2 | Add model-backed constraint extraction plus a separate deterministic repair-policy layer. | On Case 02, raw source text only produced C1-C4 automatically; the Reality Engine returned UNSAT with core C1-C4; one deadline change from 2026-09-30 to 2026-10-02 made the plan SAT. | KEEP |
Do not backfill fictional improvements. Add a row only after running and saving an experiment.
