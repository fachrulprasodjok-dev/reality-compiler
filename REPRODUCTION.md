FINAL SUBMISSION COMPLIANCE — REPRODUCTION GUIDE

Work only inside the current `reality-compiler` repository.

This is a documentation-only task.

DO NOT modify:
- solver behavior
- extraction behavior
- repair logic
- benchmark cases
- gold labels
- saved evaluation results
- reported metrics
- tests
- production code

First inspect the actual repository, including:

README.md
PROJECT_SPEC.md
IMPROVEMENT_CHANGELOG.md
requirements.txt
requirements-z3-optional.txt
baseline/
eval/
scripts/
src/
tests/
artifacts/
trajectories/

Do not invent commands, file paths, versions, runtime, cost, outputs,
model identifiers, or evaluation scripts.

Create a new root-level file:

REPRODUCTION.md

Use this structure:

# Reality Compiler — Reproduction Guide

## 1. Environment

Document the actual supported/tested environment using repository evidence.

Include:
- Python version if supported by evidence
- package installation
- API/environment requirements
- optional Z3 setup if relevant
- explain that `.env` is intentionally excluded from the submission
- never expose any actual API key

## 2. Clean Setup

Provide clean-environment setup instructions.

Use actual repository information.

Include commands like these only where accurate:

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Include a Windows activation equivalent if appropriate.

## 3. Required Data

Document the actual benchmark data.

Known project facts that must remain accurate:
- 12 frozen synthetic benchmark cases
- 7 UNSAT cases
- Case 04 is the main demonstration case

Identify the actual repository paths for:
- benchmark cases
- model-backed results
- Direct LLM baseline results
- evaluation artifacts

State that benchmark cases were frozen and were not modified after evaluation began.

## 4. Run Reality Compiler

Inspect the repository and identify the actual command or commands used
for model-backed extraction and/or Reality Compiler evaluation.

Document:
- exact command
- required input
- generated output
- output location
- expected result

Do not invent a runnable command if the repository does not contain one.
If some evidence is represented by frozen result artifacts instead,
say so transparently.

## 5. Run Direct LLM Baseline

Identify the actual command used to run the Direct LLM baseline.

Document:
- exact command
- same raw evidence
- model identifier where supported
- input
- output
- result artifact

Known aggregate results:
- feasibility classification: 12/12
- conflict localization: 7/7
- valid SAT-restoring repairs: 7/7
- boundary-minimal repairs: 4/7 = 57.1%

Only include these if supported by repository artifacts.

## 6. Run Evaluation / Comparison

Identify the real evaluation command or actual artifact-based procedure
that produces/verifies:

Reality Compiler:
- feasibility classification: 12/12
- conflict localization: 7/7
- valid repairs: 7/7
- boundary-minimal repairs: 7/7

Direct LLM:
- feasibility classification: 12/12
- conflict localization: 7/7
- valid repairs: 7/7
- boundary-minimal repairs: 4/7

Measured difference:
57.1% → 100%
+42.9 percentage points

If comparison is calculated from frozen JSONL results rather than one
runner script, explain that clearly.

Do not invent a new evaluator.

## 7. Regression Tests

Document:

python -m unittest discover -s tests -v

Expected headline output:

Ran 20 tests in <environment-dependent runtime>
OK

Do not hard-code a fake runtime.

## 8. Deterministic Gold-Solver Sanity

Document:

python scripts/run_gold_solver.py

Expected:

Gold-compiler sanity accuracy: 12/12

Explain:

The gold-solver sanity uses already-formalized benchmark constraints.
It validates the deterministic formal machinery.
It does NOT test natural-language extraction.

## 9. Formal-Engine Reproducibility

Document evidence supporting:

12 cases × 100 solver repetitions
= 1,200 solver executions

7 UNSAT cases × 100 repair repetitions
= 700 repair executions

Total:
1,900 / 1,900 stable formal-engine executions

Find the actual supporting script and/or artifact.

If an exact rerun command exists, provide it.

If only frozen evidence exists, say so transparently and cite its path.

Do not invent a repetition script.

State clearly:

This stability claim begins after extraction.

## 10. Expected Outputs

Identify actual paths for:

- frozen benchmark
- Direct LLM results
- model-backed Reality Compiler results
- comparison/evaluation result
- Case 04 Decision Receipt
- Case 04 trajectory
- changelog

Include:

artifacts/decision_receipt_case04.html

only if it exists.

## 11. Versions

Report versions only when repository evidence supports them.

Include, where available:
- Python
- OpenAI SDK
- z3-solver
- model identifier

Do not guess.

## 12. Runtime and Cost

THIS SECTION IS REQUIRED.

Separate:

### Deterministic local execution

Provide approximate runtime from actual observed executions if available.

Explain that deterministic solver/test execution does not require
model API calls.

### Model-backed execution

Provide actual recorded runtime/cost if available.

If exact historical API cost was not recorded, write clearly:

"Exact historical API cost was not recorded."

Do not invent a dollar figure.

If token/request information is available from artifacts, report it.

State that API pricing may change.

## 13. Determinism Boundary

Include prominently:

Natural-language extraction is probabilistic.

Once formal constraints are fixed, schema validation,
canonicalization, solving, repair search, and re-solving are
deterministic for the represented system.

The deterministic solver can verify only the formal world it receives.

## 14. Limitations

- MVP
- 12 synthetic benchmark cases
- 7 UNSAT
- primarily date-oriented constraints
- small formal vocabulary
- no production document ingestion
- no global business-cost optimizer
- boundary-minimal is local to the selected commitment and direction
- repairs are proposed and verified, not organizationally authorized
- human accepts, rejects, or renegotiates changes