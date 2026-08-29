# Build Sequence

## Gate 0 — frozen now
- product promise
- MVP boundary
- primary metric
- baseline prompt
- 12 synthetic cases
- gold labels and formal gold constraints
- challenge case

## Gate 1 — deterministic proof engine
- Z3 compilation
- SAT/UNSAT
- unsat core
- minimal supported repair
- automated tests

## Gate 2 — model-backed agent layer
- Extraction Agent: raw evidence → candidate constraints + evidence links
- Verification/Critic Agent: challenge extraction, missing links, entity/date normalization
- compiler validation: reject malformed/unsupported constraints
- Repair/Explanation Agent: explain solver result without altering proof

## Gate 3 — fair evaluation
- baseline on same raw evidence
- advanced on same raw evidence
- freeze model/config
- save every prediction
- measure primary + secondary metrics
- preserve failures

## Gate 4 — iteration/changelog
Potential experiments:
1. extraction only
2. extraction + verifier
3. provenance enforcement
4. second reviewer (keep only if measured improvement)
5. constrained JSON schema/tool use
6. model-generated repair vs solver-validated repair

## Gate 5 — product finish
- browser demo
- evidence cards
- constraint graph
- red UNSAT proof state
- one-click minimal repair
- rerun showing SAT after repair

## Gate 6 — submission
- README
- improvement changelog
- reproduction guide
- complete results
- trajectories for every agent
- <=5-minute video
- hot take
- final integrity/repro check
