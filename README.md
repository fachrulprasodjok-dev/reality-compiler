# Reality Compiler

> **Your project plan sounds plausible. Is it actually possible?**

Reality Compiler converts natural-language organizational commitments into formal constraints, proves whether they can coexist, identifies the commitments causing a contradiction, and searches for the smallest verified repair that restores feasibility.

Instead of asking an LLM only:

> “Does this plan look risky?”

Reality Compiler asks:

> **“Can all of these commitments mathematically be true at the same time?”**

---

## The Problem

Organizations make commitments across documents, meetings, emails, plans, policies, and teams:

- launch by September 30
- code freeze on September 25
- QA requires at least seven days after code freeze
- QA must finish before launch

Every statement sounds reasonable by itself.

Together:

```text
code freeze = Sep 25
QA >= Sep 25 + 7 days
QA >= Oct 2
QA <= launch
launch <= Sep 30