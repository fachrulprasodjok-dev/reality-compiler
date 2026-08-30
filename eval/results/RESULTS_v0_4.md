# Reality Compiler v0.4 Evaluation Result

## Result

Benchmark:

`eval/cases_v0_3/`

System:

Reality Compiler v0.4 with explicit `same_event` formal semantics and deterministic event canonicalization.

Critic Agent:

Not used.

Result:

- Correct: 12/12
- Feasibility accuracy: 100.0%
- Execution errors: 0

Raw result artifact:

`eval/results/advanced_v0_4_same_event.jsonl`

## Evaluation History

### v0.2

Original frozen benchmark:

`eval/cases/`

Result:

- 11/12 correct
- 91.7% feasibility accuracy
- 0 execution errors

Failure:

Case 04 returned false SAT.

### Benchmark Audit

Case 04 contained an unsupported semantic assumption in its frozen gold representation.

The natural-language evidence distinguished:

- security review completion
- security approval completion

while the gold model treated them as the same underlying milestone.

The original benchmark and 91.7% result were preserved unchanged.

### v0.3

A corrected, versioned benchmark was created:

`eval/cases_v0_3/`

The source evidence for Case 04 was changed to explicitly state that completion of the scheduled security review constitutes security approval.

Extraction-only evaluation still produced:

- 11/12 correct
- 91.7% feasibility accuracy
- 0 execution errors

The same corrected Case 04 passed in one run and failed in another because the extractor generated different symbols:

- `security_review`
- `security_approval`

This exposed semantic symbol instability.

### v0.4

Reality Compiler's formal constraint language was extended with:

`same_event`

Example:

`security_review SAME_EVENT security_approval`

A deterministic canonicalization stage resolves explicit event identity before feasibility solving.

The Extraction Agent was updated to emit `same_event` only when supported by explicit identity language such as:

- constitutes
- counts as
- is the same milestone as
- completion of X is completion of Y

Result on the corrected 12-case benchmark:

- 12/12 correct
- 100.0% feasibility accuracy
- 0 execution errors

## Engineering Interpretation

The improvement did not come from adding another reasoning agent.

A Constraint Critic was experimentally evaluated and rejected from the MVP after ablation showed no demonstrated benefit sufficient to justify its additional model call, latency, cost, and failure surface.

The retained architecture is:

Raw organizational evidence

→ AI constraint extraction

→ strict schema validation

→ explicit semantic relations including `same_event`

→ deterministic canonicalization

→ formal feasibility solver

→ UNSAT proof

→ minimal repair

## Scope and Limitations

The 100% result applies only to this 12-case synthetic corrected benchmark.

It is not evidence of 100% accuracy on arbitrary organizational data.

Broader and adversarial evaluation is required before making production-level accuracy claims.