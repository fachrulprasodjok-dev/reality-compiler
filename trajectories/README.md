# Reality Compiler — Agent Trajectories

This directory contains representative trajectories from the Reality Compiler build and evaluation.

The goal is to make the agent workflow inspectable from:

agent instruction

→ task / evidence

→ structured output or code action

→ tool / verifier response

→ feedback

→ retry or human checkpoint

→ final result

These trajectories intentionally exclude private chain-of-thought, credentials, and API secrets.

## Agents / agent-assisted workflows represented

### 1. Constraint Extraction Agent

Role:

Convert natural-language organizational evidence into schema-valid formal constraints.

Representative trajectory:

`01_constraint_extraction_case02.md`

Supporting raw execution:

`case_02_end_to_end.txt`

### 2. Coding / Engineering Agent Workflow

Role:

Diagnose a benchmark failure, test competing hypotheses, modify the formal representation, add regression tests, and rerun evaluation.

Representative trajectory:

`02_case04_failure_and_semantic_fix.md`

This trajectory preserves the real Case 04 progression from an incorrect SAT result to explicit `same_event` semantics and a correct UNSAT result.

### 3. Evaluation / Verification Workflow

Role:

Generate a fair structured repair baseline, apply both systems' proposed repairs to the same frozen gold constraints, and use the deterministic solver to verify repair validity and boundary minimality.

Representative trajectory:

`03_repair_evaluation_and_verification.md`

## Human checkpoints

Human approval remained in the loop for:

- accepting benchmark corrections
- deciding whether an observed failure was a model defect or benchmark defect
- freezing evaluation versions
- choosing which claims were sufficiently supported for the submission
- Git commits and pushes

No consequential organizational action is automatically executed by Reality Compiler.

## Important distinction

Runtime application traces and development-agent trajectories are different artifacts.

`case_02_end_to_end.txt` records a representative Reality Compiler execution.

The Markdown trajectories additionally capture the agent instructions, tool feedback, retries, and human checkpoints that shaped the result.