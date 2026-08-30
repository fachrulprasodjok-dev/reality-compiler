# Case 04 Critic Ablation

## Question

Did the Constraint Critic materially improve the corrected Case 04 result?

## With Critic

Corrected Case 04:

FINAL STATUS: UNSAT

UNSAT CORE: C1, C2, C3

## Without Critic

The same corrected Case 04 was run using:

Raw evidence
→ Extraction Agent
→ Schema Validation
→ Reality Engine

No Critic was used.

Result:

STATUS WITHOUT CRITIC: UNSAT

UNSAT CORE: C1, C2, C3

## Finding

The Critic was not required to achieve the correct result.

Once the source evidence explicitly stated that completion of the scheduled security review constitutes security approval, the Extraction Agent correctly represented the security milestone consistently.

## Engineering Decision

Do not include the Constraint Critic in the production MVP at this stage.

Reason:

- no demonstrated accuracy improvement on this case
- adds another model call
- increases latency
- increases cost
- increases failure surface

Preserve the Critic experiment and failure analysis as development evidence.

Reintroduce a Critic only if broader frozen evaluation demonstrates a measurable need for one.