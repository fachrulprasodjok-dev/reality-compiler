# Reality Compiler — Final Evaluation Summary v0.1

## Executive Result

Reality Compiler converts natural-language organizational commitments into formal constraints, determines whether they can coexist, identifies contradictions, and searches for a minimal repair that restores feasibility.

Evaluation used a corrected frozen synthetic benchmark of 12 cases.

The fair baseline used the same frontier model and the same raw evidence.

---

## Head-to-Head Results

| Metric | Direct LLM | Reality Compiler |
|---|---:|---:|
| Feasibility classification | 12/12 (100%) | 12/12 (100%) |
| Source-level conflict localization | 7/7 (100%) | 7/7 (100%) |
| Verified single-date repairs | 7/7 (100%) | 7/7 (100%) |
| Boundary-minimal repairs | 4/7 (57.1%) | 7/7 (100%) |
| Mean absolute date movement | 1.86 days | 1.43 days |
| Formal UNSAT proof/core | Not natively generated | Yes |
| Native repair verification loop | No | Yes |
| Deterministic formal solver | Not applicable to direct generation | Yes |
| Formal solver stability | Not measured | 1,200/1,200 |
| Repair-engine stability | Not measured | 700/700 |

---

## Primary Quantitative Differentiator

Both systems produced valid repairs for all seven UNSAT cases.

However, Reality Compiler reached the nearest satisfiable date boundary for the selected repair source and direction in:

**7/7 cases = 100%**

The structured Direct LLM baseline did so in:

**4/7 cases = 57.1%**

Difference:

**+42.9 percentage points**

Reality Compiler also moved dates less on average:

- Direct LLM: 1.86 days
- Reality Compiler: 1.43 days

This is approximately 23% less average date movement.

Boundary minimality means the smallest date movement on the same selected source-date and in the same direction that restores satisfiability.

It does not claim globally optimal organizational cost.

---

## Classification Result

Reality Compiler:

- 12/12 correct
- 100.0% feasibility classification accuracy
- 0 execution errors

Direct LLM baseline:

- 12/12 correct
- 100.0% classification accuracy
- 0 execution errors

Therefore classification accuracy is not presented as an advantage of Reality Compiler on this benchmark.

---

## Conflict Localization

There were seven UNSAT cases.

Both systems identified the exact gold source-level conflict set in:

**7/7 cases**

Metrics for both systems:

- Precision: 100%
- Recall: 100%
- F1: 100%

Therefore source-level conflict localization is not presented as an advantage on this benchmark.

---

## Repair Verification

Each system was asked to propose exactly one date change.

Both systems were evaluated by the same deterministic verifier against the frozen gold formal constraints.

Verified repairs restoring SAT:

- Direct LLM: 7/7
- Reality Compiler: 7/7

Boundary-minimal repairs:

- Direct LLM: 4/7
- Reality Compiler: 7/7

The differentiator was therefore not whether a repair could be found.

The differentiator was reaching the verified feasibility boundary rather than stopping at a merely sufficient adjustment.

---

## Formal Reproducibility

Reality Compiler separates probabilistic natural-language interpretation from deterministic formal verification.

Formal solver stress test:

- 12 constraint sets
- 100 repetitions each
- 1,200 executions
- 100% observed stability

Every repetition returned the same:

- SAT / UNSAT result
- UNSAT core

Minimal-repair stress test:

- 7 UNSAT constraint sets
- 100 repetitions each
- 700 executions
- 100% observed stability

Every repetition returned the same:

- relaxed constraint
- repair proposal
- resulting SAT status
- model dates

Combined:

**1,900 repeated formal-engine executions with 100% observed stability**

---

## Probabilistic Extraction Boundary

The entire system is not claimed to be deterministic.

A targeted five-run extraction experiment on Case 04 observed:

- 5 independent extraction calls
- 2 distinct formal representations
- explicit `same_event` in 2/5 runs
- correct final UNSAT status in 5/5 runs

One representation used explicit semantic identity:

`security_approval SAME_EVENT security_review`

Another reused the same canonical event directly:

`security_review`

Both representations encoded the relevant semantics and resulted in UNSAT.

This illustrates the architecture:

Natural-language evidence

→ probabilistic interpretation

→ formal constraints

→ deterministic verification

→ reproducible proof and repair

---

## Architecture

Raw organizational evidence

→ LLM constraint extraction

→ strict schema validation

→ explicit semantic relations such as `same_event`

→ deterministic canonicalization

→ formal SAT / UNSAT solver

→ conflict core

→ minimal repair search

→ deterministic re-verification

---

## What Reality Compiler Adds Beyond Direct LLM Reasoning

The evaluation does not show that a frontier LLM cannot recognize contradictions.

It can.

The direct baseline achieved perfect classification and localization on this small benchmark.

Reality Compiler instead adds an executable verification layer:

1. Natural-language commitments become machine-checkable constraints.
2. Contradictions become formal UNSAT results.
3. Conflict sets are traceable to source evidence.
4. Proposed repairs are mechanically applied.
5. The complete system is solved again.
6. Repair search stops at a verified feasibility boundary.
7. Once constraints are fixed, formal results are reproducible.

The value proposition is therefore not:

"AI that notices scheduling problems."

It is:

**AI that compiles organizational commitments into constraints that can be proved, repaired, and re-verified.**

---

## Limitations

The benchmark contains only 12 synthetic cases, including seven UNSAT cases.

The 100% classification result must not be generalized to arbitrary organizational data.

The 100% repair-boundary result applies only to these seven cases.

Boundary minimality is local to the selected source and movement direction.

The natural-language extraction layer remains probabilistic.

Broader adversarial, noisy-document, contradictory-source, and real-world evaluation would be required before production accuracy claims.