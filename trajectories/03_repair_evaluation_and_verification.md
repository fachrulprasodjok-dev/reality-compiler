# Trajectory 03 — Repair Evaluation and Deterministic Verification

## Purpose

Document the evaluation workflow used to compare Reality Compiler against a fair structured Direct LLM repair baseline.

This trajectory focuses on:

agent output

→ structured repair proposal

→ deterministic verification

→ boundary-minimality test

→ like-for-like comparison

→ evidence-backed human conclusion

The goal was not to assume Reality Compiler was better.

The goal was to measure:

1. whether each proposed repair actually restored feasibility,
2. whether each repair stopped at the nearest satisfiable boundary for the commitment and direction it selected, and
3. where possible, whether Reality Compiler produced a smaller adjustment when both systems selected the same commitment and movement direction.

---

## Evaluation Context

Frozen benchmark:

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

**7**

Both systems had already achieved:

```text
Feasibility classification:
12/12

Conflict localization:
7/7