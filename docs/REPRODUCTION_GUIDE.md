# Reality Compiler — Reproduction Guide

This guide reproduces the core Reality Compiler results from a fresh checkout.

Reality Compiler combines:

1. model-backed natural-language constraint extraction, and
2. deterministic formal validation, solving, conflict localization, repair, and re-verification.

The repository contains both:

- frozen submission artifacts, and
- scripts for independently rerunning the evaluation.

Some steps require OpenAI API access.

Formal solver, repair-verification, localization, and determinism checks can be run without making new model calls when using the frozen artifacts.

---

# 1. Clone the Repository

```bash
git clone https://github.com/fachrulprasodjok-dev/reality-compiler.git
cd reality-compiler