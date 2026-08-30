# Case 04 Extraction Instability

## Context

Case 04 was corrected in benchmark v0.3 so the source explicitly states:

"completing the scheduled security review constitutes security approval"

The corrected case was then tested twice using the Extraction Agent without a Critic.

## One-Off Result

The Extraction Agent represented the security milestone consistently.

Result:

UNSAT

UNSAT CORE:

C1, C2, C3

## Full Benchmark Result

During the 12-case v0.3 benchmark run, the same source evidence produced:

C1:
release <= 2026-10-15

C2:
security_review = 2026-10-16

C3:
security_approval <= release

Result:

SAT

## Root Cause

The current formal constraint language has no explicit way to represent that two differently named events are the same real-world event.

Therefore semantic identity is currently encoded implicitly through event naming.

This makes correctness dependent on whether the language model happens to choose identical event symbols across constraints.

That behavior is unstable.

## Engineering Conclusion

Do not solve this by forcing event naming through prompt wording or by adding another LLM Critic.

Instead, extend the formal language with an explicit semantic identity relation:

same_event

Example:

security_review SAME_EVENT security_approval

A deterministic canonicalization stage can then merge the two symbols before the feasibility solver runs.

## Expected Benefit

This removes feasibility correctness from dependence on model-generated variable naming and converts semantic identity into an explicit, auditable formal relation.