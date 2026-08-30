# Formal Engine Determinism Evaluation — v0.1

## Purpose

Measure reproducibility of Reality Compiler's deterministic formal layer after natural-language evidence has already been compiled into constraints.

This evaluation does not measure LLM extraction determinism.

## Input

Frozen constraints from:

`eval/results/advanced_v0_4_same_event.jsonl`

Cases:

12

Repetitions per case:

100

Total formal solver executions:

1,200

## Result

Stable cases:

12/12

Deterministic rate:

100.0%

Across all 1,200 executions, each case produced the same:

- SAT / UNSAT decision
- UNSAT core

## Interpretation

Reality Compiler separates probabilistic interpretation from deterministic verification.

Architecture:

Raw natural-language evidence

→ LLM constraint extraction

→ strict schema validation

→ deterministic canonicalization

→ deterministic formal solver

Once a constraint set is fixed, the formal feasibility decision and conflict core are reproducible.
## Minimal Repair Engine

The deterministic repair engine was also stress-tested separately.

UNSAT cases:

7

Repetitions per case:

100

Total repair executions:

700

Result:

- Stable repair cases: 7/7
- Deterministic rate: 100.0%

Across all 700 repair executions, each case reproduced the same:

- relaxed constraint selection
- repair proposal
- resulting SAT status
- model dates

## Combined Formal-Layer Result

Formal solver executions:

1,200

Repair-engine executions:

700

Total repeated formal-engine executions:

1,900

Observed stability:

100.0%

This supports the narrower claim that, once a formal constraint representation is fixed, Reality Compiler's feasibility analysis and repair generation are reproducible.

## LLM Interpretation Variability

A separate targeted experiment tested the probabilistic extraction layer.

Case:

`case_04`

Independent extraction runs:

5

Observed formal representations:

2

Explicit `same_event` emitted:

2/5

Correct final feasibility status:

5/5

Unique final statuses:

`UNSAT`

### Observed Representations

The extractor produced two semantically equivalent representations.

Representation A explicitly encoded event identity:

`security_approval SAME_EVENT security_review`

Representation B reused a common event symbol directly:

`security_review`

for both the fixed-date milestone and the before-release requirement.

Despite the representational variation, all five compiled constraint sets resolved to the correct final status:

`UNSAT`

### Interpretation

This demonstrates the architectural boundary between probabilistic interpretation and deterministic verification.

Natural-language evidence

→ probabilistic LLM interpretation

→ formal constraint representation

→ deterministic canonicalization / solving

→ reproducible feasibility result

The experiment does not establish end-to-end determinism.

Instead, it shows that multiple semantically valid formalizations were observed while the final feasibility result remained stable in this five-run sample.

## Scope and Limitations

This result does not establish that Reality Compiler is deterministic end-to-end.

The LLM extraction layer remains probabilistic and may produce different formalizations across repeated calls.

The measured 100% determinism applies only to the formal solver stage for the 12 frozen constraint sets used in this evaluation.