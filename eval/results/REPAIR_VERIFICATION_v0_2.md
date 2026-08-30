# Reality Compiler — Repair Verification v0.2

## Purpose

This revision preserves the original seven-case repair verification while adding a stricter like-for-like comparison for repair magnitude.

The original v0.1 artifacts are retained unchanged.

The correction was introduced after a case-level audit identified that Cases 03 and 06 compare repairs to different commitments moving in opposite directions.

---

## Frozen Evaluation Set

UNSAT cases:

- case_02
- case_03
- case_04
- case_06
- case_08
- case_10
- case_12

Total:

7

Both the structured Direct LLM baseline and Reality Compiler were evaluated against the same frozen gold formal constraints using the same deterministic repair verifier.

---

## 1. Repair Validity — All Seven Cases

A repair is verified when the proposed source-date change is mechanically applied to the frozen gold constraint set and the complete system re-solves to SAT.

### Direct LLM

Verified SAT repairs:

**7/7 = 100%**

### Reality Compiler

Verified SAT repairs:

**7/7 = 100%**

### Result

Repair validity is a tie on this benchmark.

---

## 2. Boundary Minimality — All Seven Proposed Repairs

Boundary minimality is evaluated within each system's selected repair:

> For the selected source/date and movement direction, no smaller date movement restores satisfiability.

This does not require both systems to select the same commitment.

It does not claim global organizational-cost optimality.

### Direct LLM

Boundary-minimal repairs:

**4/7 = 57.1%**

### Reality Compiler

Boundary-minimal repairs:

**7/7 = 100%**

Difference:

**+42.9 percentage points**

This metric remains valid across all seven cases because each proposal is evaluated against its own selected source and direction.

---

## 3. Like-for-Like Repair Comparison

A stricter subset was created for direct repair-magnitude comparison.

Cases are included only when both systems selected:

1. the same source commitment, and
2. the same movement direction.

Comparable cases:

- case_02
- case_04
- case_08
- case_10
- case_12

Total:

**n = 5**

Excluded:

- case_03
- case_06

### Why Case 03 Is Excluded

Direct LLM:

- source: V1
- 2026-10-11 → 2026-10-09
- direction: earlier
- proposed movement: 2 days

Reality Compiler:

- source: M1
- 2026-10-10 → 2026-10-11
- direction: later
- proposed movement: 1 day

The systems selected different commitments and opposite movement directions.

### Why Case 06 Is Excluded

Direct LLM:

- source: J1
- 2026-11-20 → 2026-11-18
- direction: earlier
- proposed movement: 2 days

Reality Compiler:

- source: M1
- 2026-11-26 → 2026-11-28
- direction: later
- proposed movement: 2 days

The systems again selected different commitments and opposite movement directions.

---

## 4. Like-for-Like Boundary Minimality

On the five comparable cases:

### Direct LLM

Boundary-minimal:

- case_02: no
- case_04: yes
- case_08: yes
- case_10: no
- case_12: yes

Result:

**3/5 = 60%**

### Reality Compiler

Boundary-minimal:

- case_02: yes
- case_04: yes
- case_08: yes
- case_10: yes
- case_12: yes

Result:

**5/5 = 100%**

Difference:

**+40 percentage points**

---

## 5. Like-for-Like Repair Magnitude

Only the same-source, same-direction subset is used for comparative mean date movement.

### Direct LLM

Movements:

- case_02: 3 days
- case_04: 1 day
- case_08: 2 days
- case_10: 2 days
- case_12: 1 day

Total:

9 days

Mean:

**1.80 days**

### Reality Compiler

Movements:

- case_02: 2 days
- case_04: 1 day
- case_08: 2 days
- case_10: 1 day
- case_12: 1 day

Total:

7 days

Mean:

**1.40 days**

Difference:

**0.40 days**

Relative reduction:

**22.2% lower mean movement on the five-case like-for-like subset**

Because n=5 is small, this is treated as a secondary descriptive metric rather than the primary project claim.

---

## 6. Authoritative Repair Comparison

| Metric | Direct LLM | Reality Compiler |
|---|---:|---:|
| Verified repairs — all 7 | 7/7 (100%) | 7/7 (100%) |
| Boundary-minimal — all 7 proposals | 4/7 (57.1%) | 7/7 (100%) |
| Boundary-minimal — like-for-like n=5 | 3/5 (60%) | 5/5 (100%) |
| Mean movement — like-for-like n=5 | 1.80 days | 1.40 days |

---

## 7. Interpretation

The seven-case result answers:

> Did each system stop at the satisfiable boundary for the repair it chose?

The five-case subset answers the stricter comparative question:

> When both systems chose the same commitment and moved it in the same direction, which system made the more precise adjustment?

Reality Compiler leads under both views.

However, the small benchmark size means these results should be treated as evidence from this frozen synthetic evaluation, not as a general claim about arbitrary real-world planning tasks.

---

## Reporting Correction

The v0.1 report also displayed mean movement across all seven proposals:

- Direct LLM: 1.86 days
- Reality Compiler: 1.43 days

Those values remain arithmetically correct as raw descriptive averages.

They are no longer used as a direct comparative headline because Cases 03 and 06 involve different commitments and opposite movement directions.

The submission therefore uses the five-case like-for-like subset for comparative movement reporting.