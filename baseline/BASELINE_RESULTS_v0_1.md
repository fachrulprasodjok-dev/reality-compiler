# Direct LLM Baseline — v0.1

## Purpose

Establish a fair baseline against Reality Compiler.

The baseline uses the same model and receives the same raw source evidence, but predicts feasibility directly without Reality Compiler's formal intermediate representation or deterministic solver.

## Configuration

Model:

`gpt-5.6-luna`

Benchmark:

`eval/cases_v0_3/`

Cases:

12

Input:

Raw organizational source evidence only.

Baseline architecture:

Raw evidence

→ Direct LLM reasoning

→ SAT / UNSAT

The baseline does NOT use:

- formal constraint extraction
- strict constraint schema
- `same_event`
- deterministic canonicalization
- formal feasibility solver
- solver-generated UNSAT core
- deterministic repair engine

## First Frozen Result

Correct:

12/12

Classification accuracy:

100.0%

Execution errors:

0

Average model latency:

2.206 seconds

Raw result artifact:

`baseline/direct_baseline_v0_1.jsonl`

## Interpretation

Classification accuracy alone does not distinguish the direct LLM baseline from Reality Compiler on this 12-case synthetic benchmark.

Both systems achieved 12/12 SAT/UNSAT classifications.

Therefore subsequent comparison must evaluate stronger dimensions, including:

- conflict localization
- minimal conflict identification
- proof verifiability
- repair validity
- repeatability
- auditability
- latency
- model-call cost

This baseline result is preserved unchanged and will not be weakened or rerun merely to obtain a more favorable comparison.