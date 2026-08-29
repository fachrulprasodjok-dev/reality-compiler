# Frozen Evaluation Cases

| Case | Gold | Scenario |
|---|---|---|
| 01 | SAT | Straightforward feasible launch |
| 02 | UNSAT | **Challenge:** green project, impossible QA window |
| 03 | UNSAT | Dependency lands after launch |
| 04 | UNSAT | Security approval after deadline |
| 05 | SAT | Feasible chained delivery |
| 06 | UNSAT | Two-stage testing chain exceeds launch |
| 07 | SAT | Legal approval has enough buffer |
| 08 | UNSAT | Marketing readiness later than executive commitment |
| 09 | SAT | Feasible business sign-off |
| 10 | UNSAT | Cutover rehearsal after launch deadline |
| 11 | SAT | Feasible post-freeze QA |
| 12 | UNSAT | Long hidden dependency chain |

These cases are synthetic. Their hashes are frozen in `GOLD_MANIFEST.sha256`.
