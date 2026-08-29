# Reality Compiler — Frozen MVP Specification

## Product promise
Reality Compiler turns organizational commitments expressed in natural language into a machine-verifiable constraint model.

For a supplied evidence pack it must answer:

1. **Feasibility:** SAT or UNSAT.
2. **Proof:** the smallest conflicting set it can prove, grounded to source evidence.
3. **Repair:** the smallest supported change that restores feasibility.

## Intended user
Program managers, engineering leaders, PMOs, chiefs of staff, release leaders, and strategy/operations teams coordinating interdependent commitments.

## Core failure mode
Individual statements can each look reasonable while the combined plan is impossible.

## Hackathon MVP boundary
IN:
- synthetic meeting/chat/ticket/policy evidence packs
- temporal/dependency/deadline constraints
- source-grounded proof
- minimal repair for supported editable deadlines
- fair baseline and frozen evaluation set
- representative agent trajectories

OUT until the core is proven:
- live Slack/Jira/GitHub connectors
- autonomous organizational actions
- full digital twin
- workforce optimization
- causal forecasting
- production security/multitenancy

## Architecture
Raw evidence
→ Extraction Agent (later model-backed)
→ Verification/Critic Agent
→ deterministic Constraint Compiler
→ deterministic Reality Engine (difference constraints; optional Z3 adapter)
→ unsat-core analyzer
→ deterministic repair search
→ Explanation/Repair Agent

The solver is deliberately **not** an LLM. LLMs interpret language; the formal engine proves whether the interpreted constraints can coexist.

## Primary metric
**Feasibility Classification Accuracy** = exact SAT/UNSAT matches / all frozen cases.

## Secondary metrics
- conflict-core recall
- conflict-core precision
- repair validity: applying proposed repair makes the case SAT
- source-grounding accuracy
- unsupported material claim rate
- runtime and API cost

## Fair baseline
A single-pass general-purpose model receives the exact same raw evidence pack and is asked to:
- decide SAT/UNSAT,
- identify conflicting commitments,
- suggest one repair.

It receives no solver, no structured intermediate representation, no verifier, and no constraint tools.

## Challenge case
A project is reported green. Code freeze is September 25. QA requires seven days after code freeze. Launch is committed no later than September 30. Each statement sounds normal; together they are impossible.

## Human boundary
Reality Compiler recommends and proves. It does not execute consequential changes. A qualified human approves any schedule, policy, staffing, budget, or operational change.
