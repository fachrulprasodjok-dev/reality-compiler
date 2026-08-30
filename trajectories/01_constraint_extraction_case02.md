# Trajectory 01 — Constraint Extraction Agent / Case 02

## Purpose

Representative successful end-to-end execution of the model-backed Constraint Extraction Agent followed by deterministic feasibility analysis and repair.

## Agent role

Constraint Extraction Agent

## Agent objective

Convert raw organizational evidence into formal constraint candidates that satisfy the Reality Compiler schema.

The agent does not make the final feasibility decision.

Its structured output is passed to deterministic validation and solving.

## Task

Case:

`case_02`

Scenario:

Green project status with an impossible QA window.

## Evidence supplied

The evidence establishes:

- Apollo must launch no later than 2026-09-30.
- Engineering committed to code freeze on 2026-09-25.
- QA completes no earlier than 7 days after code freeze.
- QA must finish before or on launch.

## Agent structured output

The extraction produced four formal constraints:

```text
C1 deadline
Apollo launch <= 2026-09-30

C2 fixed_date
code freeze = 2026-09-25

C3 after_days
QA completion >= code freeze + 7 days

C4 before_or_same
QA completion <= Apollo launch