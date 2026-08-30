# Case 04 Failure Analysis — v0.2

## Summary

Reality Compiler v0.2 misclassified Case 04 as SAT.

Gold result:

UNSAT

Predicted result:

SAT

## Raw semantic problem

The extracted constraints used two different event names:

- `security_review_complete`
- `security_approval_complete`

The source evidence refers to the same underlying security completion milestone.

Because the solver treats event names literally, these became two independent variables.

## Extracted structure

C1:
release <= 2026-10-15

C2:
security_review_complete = 2026-10-16

C3:
security_approval_complete <= release

## Why the solver returned SAT

The solver could satisfy the constraints by assigning different dates to the two security events.

For example:

security_approval_complete = 2026-10-14

release = 2026-10-15

security_review_complete = 2026-10-16

No formal contradiction exists unless the two security event names are resolved to the same canonical event.

## Root cause

Entity / event resolution failure.

Not a solver failure.

Not a date arithmetic failure.

Not a missing-constraint failure.

## Required architectural improvement

Add a Constraint Critic / Entity Resolution Agent between extraction and the formal solver.

Its job is to detect when differently worded event names refer to the same organizational milestone and normalize them before feasibility checking.

## Experimental implication

v0.2 result:

11/12 correct

91.7% feasibility accuracy

Case 04 is the only failure.

The next experiment will test whether adding the critic agent improves this frozen result without changing the evaluation cases.