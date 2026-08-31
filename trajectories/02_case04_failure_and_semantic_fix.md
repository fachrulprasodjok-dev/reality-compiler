# Trajectory 02 — Case 04 Failure, Diagnosis, and Semantic Fix

## Purpose

Document a real engineering failure discovered during evaluation and the feedback-driven process used to correct it.

This trajectory is intentionally not a clean success path.

It preserves the progression:

incorrect result

→ failure analysis

→ competing hypothesis

→ attempted semantic critic

→ ablation

→ benchmark clarification

→ explicit semantic representation

→ regression tests

→ post-fix model-backed result

## Initial benchmark state

Benchmark:

`eval/cases_v0_3/`

Case:

`case_04`

Title:

Security approval timing conflict

Gold status:

`UNSAT`

The relevant commitments were:

```text
M1:
Release must occur no later than 2026-10-15.

S1:
The scheduled security review completes on 2026-10-16.

P1:
Completing the scheduled security review constitutes
security approval.

P1:
Security approval must be complete before or on release.
## Reproduction Audit and Extraction-Contract Fix

A later fresh reproduction audit exposed an additional limitation.

Using the same frozen 12-case benchmark and model-backed pipeline, two observed fresh runs produced:

```text
Run A:
11/12
case_04 predicted SAT instead of UNSAT

Run B:
12/12