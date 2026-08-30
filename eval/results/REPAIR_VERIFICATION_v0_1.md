# Repair Verification Evaluation — v0.1

## Purpose

Compare a structured direct-LLM repair baseline against Reality Compiler on whether proposed single-date repairs:

1. actually restore feasibility, and
2. stop at the nearest satisfiable date boundary for the selected source and direction.

## Benchmark

`eval/cases_v0_3/`

Gold UNSAT cases:

- case_02
- case_03
- case_04
- case_06
- case_08
- case_10
- case_12

Total:

7 cases

## Verification Method

Both systems are judged by the same deterministic verifier.

For each proposed repair:

1. start from the frozen gold formal constraints,
2. apply exactly one source-date edit,
3. rerun the formal solver,
4. mark the repair verified if the resulting system is SAT.

Boundary minimality is evaluated by testing smaller day movements on the same selected source-date and in the same direction.

Therefore `boundary-minimal` does not claim global organizational-cost optimality.

## Direct LLM Baseline

Verified SAT repairs:

7/7 (100.0%)

Boundary-minimal repairs:

4/7 (57.1%)

Mean absolute date movement:

1.86 days

Non-minimal cases:

- case_02: proposed 2026-10-03; nearest SAT date was 2026-10-02
- case_03: proposed 2026-10-09; nearest SAT date was 2026-10-10
- case_10: proposed 2026-09-19; nearest SAT date was 2026-09-18

## Reality Compiler

Verified SAT repairs:

7/7 (100.0%)

Boundary-minimal repairs:

7/7 (100.0%)

Mean absolute date movement:

1.43 days

## Result

Both systems produced valid single-date repairs for all seven UNSAT cases.

Reality Compiler achieved:

- 100.0% boundary-minimal repair rate

versus:

- 57.1% for the structured direct-LLM baseline

Difference:

+42.9 percentage points.

Reality Compiler's proposed repairs also moved dates less on average:

- Reality Compiler: 1.43 days
- Direct LLM: 1.86 days

approximately 23% less average date movement.

## Interpretation

The direct LLM was strong at identifying feasible repairs.

The differentiator was not repair validity.

The differentiator was the ability to search to a formally verified feasibility boundary rather than stopping at a merely sufficient adjustment.

Reality Compiler's repair loop is:

UNSAT proof

→ select candidate relaxation

→ search repair boundary

→ rerun deterministic solver

→ stop at SAT

This provides a machine-verifiable repair certificate rather than an unverified recommendation.

## Scope and Limitations

This evaluation contains only seven synthetic UNSAT cases.

Boundary minimality is defined relative to the selected source-date and movement direction.

It does not prove globally optimal repair across every possible constraint, business cost, or organizational preference.