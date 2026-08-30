# Conflict Localization Evaluation — v0.1

## Purpose

Compare the frozen direct-LLM baseline and Reality Compiler on their ability to identify the source evidence responsible for infeasibility.

Only gold UNSAT cases were evaluated.

## Benchmark

`eval/cases_v0_3/`

UNSAT cases:

- case_02
- case_03
- case_04
- case_06
- case_08
- case_10
- case_12

Total:

7 cases

## Direct LLM

Exact conflict sets:

7/7 (100.0%)

Mean precision:

100.0%

Mean recall:

100.0%

Mean F1:

100.0%

Extra sources:

0

Missing sources:

0

## Reality Compiler

Exact conflict sets:

7/7 (100.0%)

Mean precision:

100.0%

Mean recall:

100.0%

Mean F1:

100.0%

Extra sources:

0

Missing sources:

0

## Result

Conflict localization does not differentiate the systems on this benchmark.

Both the direct LLM and Reality Compiler identified the exact gold source-level conflict set in all seven UNSAT cases.

## Interpretation

The fair direct-LLM baseline remains extremely strong.

Therefore Reality Compiler should not claim an advantage in:

- SAT/UNSAT classification accuracy on this benchmark
- source-level conflict localization on this benchmark

The next comparison should test a stronger capability:

**repair verification**

A proposed repair is valuable only if changing the stated commitment actually makes the complete constraint system satisfiable.

Reality Compiler can evaluate this deterministically by applying a proposed repair and rerunning the formal solver.

This creates an objective distinction between:

"a plausible recommendation"

and:

"a machine-verified repair that restores feasibility."