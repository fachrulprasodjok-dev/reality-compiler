# Case 04 Benchmark Defect

## Discovery

During v0.2 evaluation, Case 04 was classified SAT while the frozen gold label was UNSAT.

Initial failure analysis suspected event-alias resolution:

- `security_review_complete`
- `security_approval_complete`

A first open-ended Critic failed to merge them.

A second pairwise Critic explicitly adjudicated the pair and again concluded they were not equivalent, with high confidence.

## Source Evidence

S1:

"Security review is scheduled to complete on 2026-10-16."

P1:

"Security approval must be complete before or on the release date."

M1:

"Release must occur no later than 2026-10-15."

## Problem With Frozen Gold

The frozen gold model represents both:

- security review completion
- security approval completion

as the same event: `security_done`.

However, the supplied natural-language evidence never explicitly states that completion of the security review constitutes completion of security approval.

Therefore the original gold constraint model contains an unsupported semantic assumption.

## Why SAT Is Possible From the Evidence

A valid interpretation is:

security_approval_complete = 2026-10-14

release = 2026-10-15

security_review_complete = 2026-10-16

All explicit source statements are satisfied.

Therefore UNSAT cannot be proven from the supplied evidence alone.

## Engineering Decision

Do NOT force the Critic to merge the two events merely to match the frozen label.

Doing so would reward unsupported inference and benchmark overfitting.

The benchmark must instead be versioned and corrected transparently.

The original frozen evaluation and its 91.7% result remain preserved.

## Proposed Benchmark Correction

If the intended scenario is truly UNSAT, the source evidence must explicitly connect review completion and approval completion.

For example:

"Security approval is granted when the scheduled security review completes. The security review is scheduled to complete on 2026-10-16."

With that evidence, the formal contradiction becomes supported:

security_complete = 2026-10-16

security_complete <= release

release <= 2026-10-15

Therefore:

UNSAT