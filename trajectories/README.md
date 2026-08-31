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

## Agent coverage and deterministic components

The submitted trajectories distinguish model-backed or development-agent activity from deterministic runtime software.

- **Constraint Extraction Agent** — model-backed and probabilistic; proposes formal constraints from natural-language evidence.
- **Coding / Engineering Agent Workflow** — development-time agent workflow used to diagnose the Case 04 failure, test alternatives, implement the retained fix, and validate it.
- **Direct LLM repair baseline / evaluation workflow** — model-backed evaluation comparator used for the fair baseline comparison.
- **Semantic critic** — experimental model-backed approach evaluated during the Case 04 investigation and not retained in the final system; documented in the Case 04 failure-and-fix trajectory.

The following runtime components are deterministic software modules, not agents:

- schema validation
- semantic canonicalization
- SAT / UNSAT solving
- conflict-core computation
- repair search
- complete-system re-solving
- Decision Receipt generation

Artificial agent trajectories are not created for deterministic software modules.

## Human checkpoints
Human approval remained in the loop for:

- reviewing benchmark validity and freezing evaluation versions before final comparison
- deciding whether an observed failure was a model defect or benchmark defect
- choosing which claims were sufficiently supported for the submission
- Git commits and pushes

No consequential organizational action is automatically executed by Reality Compiler.

## Important distinction

Runtime application traces and development-agent trajectories are different artifacts.

`case_02_end_to_end.txt` records a representative Reality Compiler execution.

The Markdown trajectories additionally capture the agent instructions, tool feedback, retries, and human checkpoints that shaped the result.