# Improvement Changelog

This file starts **before** model experiments so we preserve the real development story.

| Stage | Hypothesis/change | Evidence | Decision |
|---|---|---|---|
| v0 | Separate natural-language interpretation from formal feasibility proof. Freeze benchmark before model tuning. | 12 synthetic gold cases + solver sanity check | IN PROGRESS |
| v0.1 | Add a strict constraint schema and validator between AI extraction and the formal solver. | Case 02 gold constraints accepted; unsupported `probably_delayed` output rejected; duplicate IDs rejected; automated suite passes 7/7 tests. | KEEP |
| v0.2 | Add model-backed constraint extraction plus a separate deterministic repair-policy layer. | On Case 02, raw source text only produced C1-C4 automatically; the Reality Engine returned UNSAT with core C1-C4; one deadline change from 2026-09-30 to 2026-10-02 made the plan SAT. | KEEP |
| v0.2-eval | Run the model-backed extraction pipeline across all 12 frozen evaluation cases before adding a critic agent. | 11/12 feasibility classifications correct = 91.7%; 0 execution errors. Case 04 was the only failure: `security_review_complete` and `security_approval_complete` were treated as different events, causing a false SAT result. | PRESERVE AS PRE-CRITIC BASELINE |
| v0.3a | Add first Constraint Critic for open-ended event-equivalence discovery. | On Case 04 the Critic returned an empty equivalence list and failed to resolve `security_review_complete` vs `security_approval_complete`; false SAT would remain. | REJECT — replace with pairwise adjudication |
| v0.3b | Replace passive alias discovery with explicit pairwise event adjudication. | On Case 04 the Critic again rejected equivalence between `security_review_complete` and `security_approval_complete` with 90%+ confidence. Review of the source showed the frozen gold itself assumed an unstated equivalence. | KEEP CRITIC; FLAG BENCHMARK DEFECT |
| v0.3c | Ablate the Critic by rerunning corrected Case 04 with Extraction Agent + solver only. | Without the Critic, Case 04 still returned UNSAT with core C1-C3. The Critic therefore provided no demonstrated benefit while adding model cost and latency. | REJECT CRITIC FROM MVP; PRESERVE EXPERIMENT |
| v0.3d | Re-run corrected benchmark v0.3 with Extraction Agent only. | Result remained 11/12 = 91.7%. Case 04 passed in a one-off run but failed in the full run because the same evidence produced `security_review` and `security_approval` as separate symbols. | KEEP FINDING — add explicit `same_event` formal primitive |
| v0.4 | Add explicit `same_event` semantics plus deterministic canonicalization; update extraction schema/instructions to emit identity only when explicitly supported by source evidence. | Corrected 12-case benchmark: 12/12 feasibility classifications correct = 100.0%; 0 execution errors. Previous v0.3 run on the same corrected benchmark was 11/12 = 91.7%. | KEEP |
Do not backfill fictional improvements. Add a row only after running and saving an experiment.
