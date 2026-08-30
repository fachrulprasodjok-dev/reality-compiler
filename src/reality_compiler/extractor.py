import json
import os

from openai import OpenAI

from .schemas import validate_constraints


DEFAULT_MODEL = os.getenv(
    "REALITY_COMPILER_MODEL",
    "gpt-5.6-luna",
)


EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "constraints": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                    },
                    "kind": {
                        "type": "string",
                        "enum": [
                            "deadline",
                            "fixed_date",
                            "earliest",
                            "after_days",
                            "before_or_same",
                            "same_event",
                        ],
                    },
                    "event": {
                        "type": "string",
                    },
                    "date": {
                        "type": ["string", "null"],
                    },
                    "ref": {
                        "type": ["string", "null"],
                    },
                    "days": {
                        "type": ["integer", "null"],
                    },
                    "source_id": {
                        "type": "string",
                    },
                    "description": {
                        "type": "string",
                    },
                },
                "required": [
                    "id",
                    "kind",
                    "event",
                    "date",
                    "ref",
                    "days",
                    "source_id",
                    "description",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": ["constraints"],
    "additionalProperties": False,
}


INSTRUCTIONS = """
You are the Fact & Constraint Extraction Agent for Reality Compiler.

Your job is ONLY to translate explicit organizational evidence into
formal constraints.

Do not decide whether the plan is feasible.
Do not calculate SAT or UNSAT.
Do not recommend repairs.
Do not invent facts.

Use only information explicitly present in the supplied sources.

Allowed constraint kinds:

1. deadline
   Meaning:
   event must occur no later than an absolute date.

   Example:
   "Launch must happen by September 30."
   ->
   kind = deadline
   event = launch
   date = 2026-09-30

2. fixed_date
   Meaning:
   event is explicitly committed to an exact date.

   Example:
   "Code freeze is September 25."
   ->
   kind = fixed_date
   event = code_freeze
   date = 2026-09-25

3. earliest
   Meaning:
   event cannot occur before an absolute date.

4. after_days
   Meaning:
   one event can complete only after another event plus
   a stated number of days.

   Example:
   "QA completes no earlier than 7 days after code freeze."
   ->
   kind = after_days
   event = qa_complete
   ref = code_freeze
   days = 7

5. before_or_same
   Meaning:
   one event must occur before or on another event.

   Example:
   "QA must finish before launch."
   ->
   kind = before_or_same
   event = qa_complete
   ref = launch
6. same_event
   Meaning:
   two different event names explicitly refer to the same
   organizational occurrence or milestone.

   Use this ONLY when the source explicitly states semantic identity,
   equivalence, or that completing one event constitutes another event.

   Example:
   "Completing the scheduled security review constitutes
   security approval."
   ->
   kind = same_event
   event = security_approval
   ref = security_review_complete

   Example:
   "Final business sign-off is the same event as executive approval."
   ->
   kind = same_event
   event = business_signoff
   ref = executive_approval

   Do not use same_event merely because two events are related,
   ordered, dependent, or likely to happen together.

Important rules:

- Split compound statements into separate constraints.
- Preserve every source_id exactly.
- Every material constraint must point to its supporting source.
- Use snake_case event names.
- Assign IDs sequentially: C1, C2, C3...
- Ignore status language such as "green", "red", "on track",
  "high risk", or opinions unless it creates a formal constraint.
- Never infer a date, duration, dependency, or policy that is not stated.
- If a field does not apply, return null for that field.
- Preserve explicit semantic identity.
  If the evidence explicitly says that one named event constitutes,
  equals, means, or is the same occurrence as another named event,
  represent that relationship using same_event unless both facts
  already intentionally use the exact same event symbol.

- Before returning, check every compound source for explicit
  equivalence or constitutive relationships and ensure that each
  material relationship is represented formally.

- Do not infer same_event from similarity alone.
"""


def _remove_null_fields(constraint):
    return {
        key: value
        for key, value in constraint.items()
        if value is not None
    }


def extract_constraints(sources, model=DEFAULT_MODEL):
    client = OpenAI()

    response = client.responses.create(
        model=model,
        instructions=INSTRUCTIONS,
        input=json.dumps(
            {
                "sources": sources,
            },
            indent=2,
        ),
        text={
            "format": {
                "type": "json_schema",
                "name": "reality_compiler_constraints",
                "strict": True,
                "schema": EXTRACTION_SCHEMA,
            }
        },
        store=False,
    )

    result = json.loads(response.output_text)

    constraints = [
        _remove_null_fields(item)
        for item in result["constraints"]
    ]

    validate_constraints(constraints)

    return constraints