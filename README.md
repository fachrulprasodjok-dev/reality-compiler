# Reality Compiler

> **Compile organizational language into a verifiable model of reality.**

Reality Compiler is a hackathon MVP that detects when a set of project commitments cannot all be true at the same time, shows the evidence-backed conflict, and proposes the smallest supported repair.

## Why this exists

Organizations coordinate through meetings, tickets, policies, roadmaps and messages. Most tools summarize those artifacts. Reality Compiler asks a harder question:

> **Can all of these commitments actually coexist?**

The system separates language interpretation from proof:

```text
Evidence → Agent extraction/verification → Formal constraints → Solver
        → SAT / UNSAT → conflict proof → minimal repair → explanation
```

## Current starter state

This starter freezes the product scope and synthetic benchmark first. The deterministic formal constraint engine is executable now on gold constraints. An optional Z3 adapter is reserved for a later experiment. The next build stage is the model-backed Extraction + Verification agents operating on the same frozen raw evidence.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/run_gold_solver.py
python -m unittest discover -s tests -v
```

## Important
Do **not** change the frozen gold labels to make later predictions look better. If the benchmark must change, version it explicitly.
