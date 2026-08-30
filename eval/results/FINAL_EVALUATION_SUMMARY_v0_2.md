# Reality Compiler — Final Evaluation Summary v0.2

## Status

This is the corrected submission-facing evaluation summary.

It preserves the frozen v0.1 evaluation artifacts while adding a stricter like-for-like repair comparison after a case-level audit identified a comparability limitation in the original mean-movement reporting.

The underlying benchmark predictions and repair outputs were not changed.

---

# Executive Result

Reality Compiler and the Direct LLM baseline both performed strongly on the frozen 12-case synthetic benchmark.

## Feasibility Classification

Direct LLM:

**12/12 = 100%**

Reality Compiler:

**12/12 = 100%**

Result:

**Tie**

---

## Conflict Localization

Seven cases were UNSAT.

Direct LLM exact conflict localization:

**7/7 = 100%**

Reality Compiler exact conflict localization:

**7/7 = 100%**

Result:

**Tie**

---

## Verified Repairs

Both systems produced one-date repairs that restored satisfiability in every UNSAT case.

Direct LLM:

**7/7 = 100%**

Reality Compiler:

**7/7 = 100%**

Result:

**Tie**

---

# Primary Repair-Precision Result

Boundary minimality is defined as:

> For the selected source/date and movement direction, no smaller date adjustment restores satisfiability.

This is a per-proposal measure.

It does not claim global organizational-cost optimality.

## All Seven UNSAT Cases

Direct LLM:

**4/7 = 57.1%**

Reality Compiler:

**7/7 = 100%**

Difference:

**+42.9 percentage points**

This result answers:

> For the repair each system chose, did it stop at the nearest satisfiable boundary?

---

# Strict Like-for-Like Repair Comparison

A case-level audit identified two cases where the systems selected different commitments and opposite movement directions:

- case_03
- case_06

Those cases remain valid for per-proposal boundary-minimality evaluation, but they are excluded from direct repair-magnitude comparison.

The strict comparable subset therefore includes:

- case_02
- case_04
- case_08
- case_10
- case_12

Total:

**n = 5**

## Boundary Minimality — Comparable Subset

Direct LLM:

**3/5 = 60%**

Reality Compiler:

**5/5 = 100%**

Difference:

**+40 percentage points**

## Mean Date Movement — Comparable Subset

Direct LLM:

**1.80 days**

Reality Compiler:

**1.40 days**

Difference:

**0.40 days**

Relative reduction:

**22.2% lower mean movement for Reality Compiler**

Because the comparable subset contains only five cases, mean movement is treated as a secondary descriptive result rather than the primary project claim.

---

# Why Cases 03 and 06 Are Excluded from Movement Comparison

## Case 03

Direct LLM:

```text
source: V1
2026-10-11 -> 2026-10-09
direction: earlier
movement: 2 days