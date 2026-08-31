# Reality Compiler

> **Your project plan sounds plausible. Is it actually possible?**

Reality Compiler turns natural-language organizational commitments into a formal verification problem.

It uses an LLM to interpret evidence, then deterministic machinery to decide whether the resulting commitments can coexist, identify a contradiction, search for a boundary-minimal repair, re-solve the system, and produce a human-readable **Feasibility Decision Receipt**.

> **AI proposes meaning. Deterministic machinery decides feasibility.**

---

## 60-second summary

```text
RAW ORGANIZATIONAL EVIDENCE
        ↓
MODEL-BACKED CONSTRAINT EXTRACTION
        ↓
STRICT SCHEMA VALIDATION
        ↓
SEMANTIC CANONICALIZATION
        ↓
DETERMINISTIC FORMAL SOLVER
        ↓
SAT / UNSAT
        ↓
UNSAT CONFLICT CORE
        ↓
MINIMAL REPAIR SEARCH
        ↓
RE-SOLVE
        ↓
VERIFIED SAT REPAIR
        ↓
FEASIBILITY DECISION RECEIPT
```

### Frozen evaluation

| Metric | Direct LLM | Reality Compiler |
|---|---:|---:|
| Feasibility classification | 12/12 | 12/12 |
| Conflict localization | 7/7 | 7/7 |
| Verified SAT-restoring repairs | 7/7 | 7/7 |
| Boundary-minimal repairs | 4/7 | **7/7** |

**Primary measured difference:**
Reality Compiler: **100% boundary-minimal**
Direct LLM: **57.1% boundary-minimal**

Difference: **+42.9 percentage points**

For the stricter like-for-like subset where both systems chose the same source and movement direction:

| Metric | Direct LLM | Reality Compiler |
|---|---:|---:|
| Boundary-minimal | 3/5 | **5/5** |
| Mean date movement | 1.80 days | **1.40 days** |

Additional evidence:

```text
Formal-engine executions:
1,900 / 1,900 observed stable

Case 04 targeted robustness:
10 / 10 correct UNSAT
10 / 10 semantic coverage
0 retries
0 manual corrections

Regression suite:
20 / 20 passing
```

Reality Compiler does **not** claim that the Direct LLM could not solve the benchmark. It did.

The difference is that Reality Compiler turns the answer into something that can be **formally checked, traced, repaired, and mechanically re-verified**.

---

# The problem

Organizations distribute commitments across:

- project plans
- executive decisions
- emails and meeting notes
- policies
- security requirements
- vendor milestones
- approval gates
- QA and migration plans

Each statement may look reasonable independently.

The combined set may be impossible.

For example:

```text
Release must occur no later than 15 Oct 2026.

Security review completes on 16 Oct 2026.

Completing the scheduled security review
constitutes security approval.

Security approval must be complete
before or on the release date.
```

Reality Compiler represents that as:

```text
release <= 2026-10-15

security_review_complete = 2026-10-16

security_approval SAME_EVENT security_review_complete

security_approval <= release
```

The formal result is:

```text
UNSAT
```

Reality Compiler then identifies the conflict and searches for an allowed repair.

For this case:

```text
Move release deadline:

2026-10-15
        ↓
2026-10-16
```

The full represented system is solved again.

Result:

```text
SAT
```

---

# What the user receives

Reality Compiler produces a **Feasibility Decision Receipt** rather than stopping at terminal output or raw JSON.

The Case 04 receipt reports:

```text
NOT FEASIBLE

Why:
Release is committed by 15 Oct 2026,
but required security approval cannot exist
until the security review completes on 16 Oct 2026.

Conflict evidence:
M1
S1
P1

Verification trace:
C1 · C2 · C4

MINIMAL VERIFIED REPAIR

Move release deadline:
2026-10-15 → 2026-10-16

Boundary-minimal:
No smaller date adjustment on this selected
commitment and direction restores feasibility.

AFTER REPAIR:
FEASIBLE — SAT
```

It also explicitly preserves the human decision boundary:

> **Human decision required:** accept, reject, or renegotiate the proposed commitment change.

Artifacts:

```text
artifacts/decision_receipt_case04.html
artifacts/decision_receipt_case04.md
```

Generate it with:

```bash
python scripts/generate_decision_receipt.py \
  --case eval/cases_v0_3/case_04.json \
  --results eval/results/model_backed_postfix_v0_1.jsonl \
  --markdown-output artifacts/decision_receipt_case04.md \
  --html-output artifacts/decision_receipt_case04.html
```

---

# Why not just ask an LLM?

That was tested directly.

The fair Direct LLM baseline received:

- the same raw evidence
- the same frozen cases
- the same model family

The frozen model-backed evaluation used:

```text
gpt-5.6-luna
```

The Direct LLM achieved:

```text
12/12 feasibility classification
7/7 conflict localization
7/7 valid SAT-restoring repairs
```

So the project's claim is **not**:

> “LLMs cannot reason about these contradictions.”

The project found the opposite.

The distinction is architectural.

### Direct LLM

```text
Evidence
   ↓
LLM reasoning
   ↓
Answer
```

### Reality Compiler

```text
Evidence
   ↓
LLM interpretation
   ↓
formal constraints
   ↓
schema validation
   ↓
semantic canonicalization
   ↓
deterministic solver
   ↓
conflict proof
   ↓
repair search
   ↓
mechanical re-verification
```

Reality Compiler separates:

```text
probabilistic interpretation
```

from:

```text
deterministic verification
```

---

# The measured repair advantage

Reality Compiler's primary quantitative differentiator is **boundary minimality**.

For the selected source/date and movement direction, a repair is boundary-minimal when:

> No smaller date adjustment restores satisfiability.

This is deliberately narrower than global business optimization.

Reality Compiler does **not** claim:

- globally optimal organizational repair
- minimum business cost
- minimum risk
- minimum economic impact

Across all seven frozen UNSAT cases:

```text
Direct LLM:
4/7 boundary-minimal
57.1%

Reality Compiler:
7/7 boundary-minimal
100%
```

Both systems restored SAT in all seven cases.

Reality Compiler more consistently stopped exactly at the nearest satisfiable boundary.

## Like-for-like subset

`case_03` and `case_06` used different commitments and/or movement directions between systems.

Their per-system minimality scores remain valid, but raw movement magnitude is not treated as an apples-to-apples comparison.

For the five cases where both systems chose the same source and direction:

```text
Direct LLM:
3/5 boundary-minimal
mean movement 1.80 days

Reality Compiler:
5/5 boundary-minimal
mean movement 1.40 days
```

Detailed evaluation:

```text
eval/results/REPAIR_VERIFICATION_v0_2.md
eval/results/FINAL_EVALUATION_SUMMARY_v0_2.md
```

---

# The failure that changed the architecture

The first end-to-end evaluation achieved:

```text
11/12
91.7%
```

The failed case was `case_04`.

The deterministic solver was not the primary problem.

The model extracted:

```text
security_review_complete
```

and:

```text
security_approval
```

as separate symbols without preserving the evidence that:

```text
completing the security review
constitutes security approval
```

The project initially experimented with a semantic critic.

That approach was not retained.

Instead, the missing meaning was promoted into the formal vocabulary:

```text
same_event
```

and handled by a deterministic canonicalization layer.

This turned:

```text
"hope the model internally reasons about identity"
```

into:

```text
"represent identity explicitly,
inspect it,
test it,
canonicalize it"
```

The corrected frozen evaluation achieved:

```text
12/12
```

---

# A reproduction audit exposed a second issue

During final fresh reproduction testing, observed pre-fix model-backed runs produced:

```text
11/12
12/12
```

The varying case was again `case_04`.

Source inspection found that `same_event` was supported by:

- the extraction JSON schema
- schema validation
- canonicalization
- solver integration

but was not explicitly defined in the extraction-agent instructions.

The extraction contract was corrected.

Three regression protections were added.

No generic retry loop was added.

The decision was:

> Test the smallest correction first. Add orchestration only if evidence justifies it.

---

# Prospective Case 04 robustness probe

Before observing the result, a targeted test was defined:

```text
10 independent extraction runs
0 retries
0 manual correction
gold label not supplied to the model
```

Observed:

| Metric | Result |
|---|---:|
| Correct final UNSAT | **10/10** |
| Semantic coverage | **10/10** |
| Explicit `same_event` | **10/10** |
| Distinct formalizations | 2 |
| Errors | 0 |

Artifact:

```text
eval/results/CASE04_SEMANTIC_ROBUSTNESS_v0_1.json
```

The two distinct formalizations matter.

They demonstrate that model-backed extraction remained probabilistic even though all ten sampled runs preserved the material semantic relationship.

One subsequent full post-fix model-backed benchmark was then run:

```text
12/12 correct
100.0% feasibility accuracy
0 errors
```

Artifact:

```text
eval/results/model_backed_postfix_v0_1.jsonl
```

This does **not** establish deterministic natural-language extraction.

---

# Deterministic reproducibility

The formal engine was tested independently from model extraction.

### Solver

```text
12 cases × 100 repetitions
=
1,200 executions
```

Observed:

```text
1,200 / 1,200 stable
```

Same:

- SAT / UNSAT result
- UNSAT core

### Repair engine

```text
7 UNSAT cases × 100 repetitions
=
700 executions
```

Observed:

```text
700 / 700 stable
```

Same:

- relaxed constraint
- repair proposal
- resulting SAT state
- model dates

### Combined

```text
1,900 repeated formal-engine executions
100% observed stability
```

This reproducibility claim applies **after formal constraints are fixed**.

It is not a claim that the LLM extraction stage is deterministic.

---

# Clean-clone reproduction

The submission was tested from a fresh repository checkout and fresh virtual environment.

The audit reproduced:

```text
dependency installation
        ✓

20/20 regression tests
        ✓

gold-solver sanity
12/12
        ✓

Decision Receipt regeneration
        ✓
```

The first clean-clone receipt attempt exposed a committed indentation defect in the generator.

That defect was fixed, the complete path was rerun, and the corrected generator was pushed.

This is why reproducibility was tested rather than assumed.

---

# Architecture

Core implementation:

```text
src/reality_compiler/
```

### `extractor.py`

Model-backed translation of raw organizational evidence into structured constraints.

### `schemas.py`

Strict validation before formal solving.

### `canonicalizer.py`

Deterministic resolution of explicit semantic identity, including `same_event`.

### `solver.py`

Formal SAT / UNSAT feasibility engine.

### `repair_policy.py`

Defines which commitments are editable or renegotiable.

### `repair.py`

Searches editable relaxations and returns a SAT-restoring repair.

### `receipt.py`

Turns the verified machine result into a human-facing Feasibility Decision Receipt.

---

# Current formal vocabulary

The MVP supports:

```text
deadline
fixed_date
earliest
after_days
before_or_same
same_event
```

Example:

```text
deadline:
launch <= 2026-09-30

fixed_date:
code_freeze = 2026-09-25

after_days:
qa_complete >= code_freeze + 7

before_or_same:
qa_complete <= launch

same_event:
security_approval = security_review_complete
```

---

# Evaluation

Frozen benchmark:

```text
eval/cases_v0_3/
```

Cases:

```text
12 total
7 UNSAT
5 SAT
```

The benchmark is synthetic.

Synthetic cases were used so that the exact commitment structure, gold feasibility state, and expected contradictions could be controlled and inspected.

Key evidence:

```text
eval/results/FINAL_EVALUATION_SUMMARY_v0_2.md
eval/results/REPAIR_VERIFICATION_v0_2.md
eval/results/CASE04_SEMANTIC_ROBUSTNESS_v0_1.json
eval/results/model_backed_postfix_v0_1.jsonl
eval/results/DETERMINISM_RESULTS_v0_1.md
eval/results/LOCALIZATION_RESULTS_v0_1.md
```

---

# Tests

Current regression suite:

```text
20 tests
20/20 passing
```

Coverage includes:

- schema validation
- formal solver behavior
- SAT and UNSAT cases
- same-event canonicalization
- chained same-event relationships
- hidden-conflict exposure
- extractor-contract protections
- Decision Receipt generation

Run:

```bash
python -m unittest discover -s tests -v
```

---

# Quick reproduction

Clone:

```bash
git clone https://github.com/fachrulprasodjok-dev/reality-compiler.git
cd reality-compiler
```

Create environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install:

```bash
pip install -r requirements.txt
```

Optional Z3 adapter:

```bash
pip install -r requirements-z3-optional.txt
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

Run deterministic gold sanity:

```bash
python scripts/run_gold_solver.py
```

Expected:

```text
Gold-compiler sanity accuracy: 12/12
```

Generate the Decision Receipt:

```bash
python scripts/generate_decision_receipt.py \
  --case eval/cases_v0_3/case_04.json \
  --results eval/results/model_backed_postfix_v0_1.jsonl \
  --markdown-output artifacts/decision_receipt_case04.md \
  --html-output artifacts/decision_receipt_case04.html
```

Model-backed evaluation requires API access:

```bash
python scripts/run_ai_all_cases.py \
  --cases-dir eval/cases_v0_3 \
  --output eval/results/reproduction_run.jsonl
```

Model-backed extraction is probabilistic.

The deterministic formal engine begins **after extraction**.

Full instructions:

```text
docs/REPRODUCTION_GUIDE.md
```

---

# Agent trajectories

Representative execution trajectories are in:

```text
trajectories/
```

Included:

```text
01_constraint_extraction_case02.md
02_case04_failure_and_semantic_fix.md
03_repair_evaluation_and_verification.md
```

They document:

- model role
- raw evidence
- structured output
- validation
- deterministic solver result
- observed failures
- engineering decisions
- repair verification
- human checkpoints

They intentionally exclude private chain-of-thought and API secrets.

---

# Engineering changelog

Evidence-backed development decisions are recorded in:

```text
IMPROVEMENT_CHANGELOG.md
```

The changelog is structured around:

```text
experiment
    ↓
evidence
    ↓
decision
```

rather than only recording code changes.

---

# Real-world target applications

Reality Compiler is not yet deployed in production.

The architecture is intended for areas such as:

- product and software launches
- enterprise transformation programs
- security and compliance gates
- vendor and procurement delivery
- data/cloud/core-platform migrations
- regulatory and audit-sensitive programs
- M&A and integration programs
- AI-agent pre-flight validation

The common pattern is the same:

> Multiple individually plausible commitments must all be true at once.

---

# Limitations

Reality Compiler is an MVP.

Current limitations:

- 12 synthetic benchmark cases
- 7 UNSAT repair cases
- primarily date-oriented constraints
- limited formal vocabulary
- probabilistic natural-language extraction
- no production document-ingestion layer
- no global business-cost optimizer
- no claim of globally optimal repair
- no claim of 100% real-world accuracy
- no guarantee that every material fact is extracted
- additional adversarial and real-world testing is required

The most important limitation is also the most important lesson:

> **The deterministic solver can verify only the formal world it receives.**

If extraction omits material meaning, the formal verifier cannot independently recover that missing fact.

Reality Compiler exposes that boundary rather than hiding it.

---

# What Reality Compiler does not claim

It is not:

- an autonomous project manager
- a scheduling chatbot
- proof that LLMs cannot reason about contradictions
- a globally optimal business-repair engine
- a production-ready enterprise platform
- a replacement for human decision-makers

It is:

> **a verification layer between probabilistic AI interpretation and consequential organizational decisions.**

---

# The project insight

The project started with an assumption:

> A Direct LLM would struggle on these contradictions.

That assumption was wrong.

The Direct LLM performed extremely well.

That changed the engineering question from:

> “Can AI spot the contradiction?”

to:

> **“What should deterministic machinery add when the AI already understands the contradiction?”**

Reality Compiler's answer is:

```text
formalization
verification
traceability
minimality testing
reproducibility
mechanical re-verification
```

Case 04 exposed the deeper boundary:

> **Formal verification proves the consequences of what the AI compiled. Semantic completeness at the probabilistic-to-formal boundary is itself an engineering problem.**

That is the frontier Reality Compiler explores.

## Reproduction

For clean-environment setup, exact baseline, solution, and evaluation procedures, expected outputs, versions, runtime, and cost notes, see [REPRODUCTION.md](REPRODUCTION.md).

---

## One-line summary

> **Reality Compiler turns AI-interpreted organizational commitments into a deterministic verification problem, so contradictions and repairs can be mechanically checked rather than merely asserted.**