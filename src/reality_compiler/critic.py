import json
from itertools import combinations

from openai import OpenAI

from .extractor import DEFAULT_MODEL


PAIRWISE_SCHEMA = {
    "type": "object",
    "properties": {
        "decisions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "event_a": {
                        "type": "string",
                    },
                    "event_b": {
                        "type": "string",
                    },
                    "equivalent": {
                        "type": "boolean",
                    },
                    "confidence": {
                        "type": "integer",
                    },
                    "evidence_source_ids": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
                    },
                    "reason": {
                        "type": "string",
                    },
                },
                "required": [
                    "event_a",
                    "event_b",
                    "equivalent",
                    "confidence",
                    "evidence_source_ids",
                    "reason",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": [
        "decisions"
    ],
    "additionalProperties": False,
}


INSTRUCTIONS = """
You are the Constraint Critic / Event Resolution Agent
for Reality Compiler.

You receive:

1. original source evidence
2. formal constraints produced by another agent
3. explicit candidate pairs of event names

Your ONLY job is to adjudicate every candidate pair:

Do these two event names refer to the SAME real-world
organizational milestone?

Return one decision for EVERY supplied pair.

Do not determine SAT or UNSAT.
Do not change dates.
Do not invent dependencies.
Do not propose repairs.

Be conservative.

Equivalent means the two names describe the same underlying
event or completion milestone in the supplied evidence.

Examples of potentially equivalent wording:

- design_review_complete
- design_approval_complete

These may be equivalent ONLY if the evidence indicates that
approval is the completion outcome of that same design review.

Examples of NOT equivalent events:

- qa_complete
- launch

They may be related by dependency, but they are separate events.

- code_freeze
- qa_complete

These are separate milestones.

Rules:

- Evaluate every candidate pair supplied.
- Never introduce event names that were not supplied.
- Related events are not automatically equivalent.
- Sequential events are not equivalent.
- Use source evidence and constraint descriptions together.
- confidence must be an integer from 0 to 100.
- evidence_source_ids must contain only relevant supplied sources.
"""


def _known_events(constraints):
    events = set()

    for constraint in constraints:
        event = constraint.get("event")

        if event:
            events.add(event)

        ref = constraint.get("ref")

        if ref:
            events.add(ref)

    return sorted(events)


def _candidate_pairs(constraints):
    events = _known_events(
        constraints
    )

    return [
        {
            "event_a": event_a,
            "event_b": event_b,
        }
        for event_a, event_b
        in combinations(events, 2)
    ]


def adjudicate_event_pairs(
    sources,
    constraints,
    model=DEFAULT_MODEL,
):
    candidate_pairs = _candidate_pairs(
        constraints
    )

    if not candidate_pairs:
        return []

    client = OpenAI()

    response = client.responses.create(
        model=model,
        instructions=INSTRUCTIONS,
        input=json.dumps(
            {
                "sources": sources,
                "constraints": constraints,
                "candidate_pairs": candidate_pairs,
            },
            indent=2,
        ),
        text={
            "format": {
                "type": "json_schema",
                "name": "pairwise_event_adjudication",
                "strict": True,
                "schema": PAIRWISE_SCHEMA,
            }
        },
        store=False,
    )

    result = json.loads(
        response.output_text
    )

    decisions = result[
        "decisions"
    ]

    expected_pairs = {
        tuple(sorted([
            pair["event_a"],
            pair["event_b"],
        ]))
        for pair in candidate_pairs
    }

    returned_pairs = set()

    known_sources = {
        source["id"]
        for source in sources
    }

    for decision in decisions:
        event_a = decision[
            "event_a"
        ]

        event_b = decision[
            "event_b"
        ]

        pair = tuple(sorted([
            event_a,
            event_b,
        ]))

        if pair not in expected_pairs:
            raise ValueError(
                "Critic returned an unknown "
                f"event pair: {pair}"
            )

        if pair in returned_pairs:
            raise ValueError(
                "Critic returned duplicate "
                f"event pair: {pair}"
            )

        returned_pairs.add(
            pair
        )

        confidence = decision[
            "confidence"
        ]

        if not 0 <= confidence <= 100:
            raise ValueError(
                "Critic confidence must "
                "be between 0 and 100"
            )

        evidence_ids = set(
            decision[
                "evidence_source_ids"
            ]
        )

        if not evidence_ids.issubset(
            known_sources
        ):
            raise ValueError(
                "Critic returned unknown "
                "source IDs"
            )

    if returned_pairs != expected_pairs:
        missing = (
            expected_pairs
            - returned_pairs
        )

        raise ValueError(
            "Critic omitted candidate "
            f"pairs: {sorted(missing)}"
        )

    return decisions


def _build_resolution(
    decisions,
    min_confidence=80,
):
    parents = {}

    def find(item):
        parents.setdefault(
            item,
            item,
        )

        if parents[item] != item:
            parents[item] = find(
                parents[item]
            )

        return parents[item]

    def union(a, b):
        root_a = find(a)
        root_b = find(b)

        if root_a != root_b:
            canonical = min(
                root_a,
                root_b,
            )

            other = max(
                root_a,
                root_b,
            )

            parents[
                other
            ] = canonical

    for decision in decisions:
        event_a = decision[
            "event_a"
        ]

        event_b = decision[
            "event_b"
        ]

        find(event_a)
        find(event_b)

        if (
            decision["equivalent"]
            and decision["confidence"]
            >= min_confidence
        ):
            union(
                event_a,
                event_b,
            )

    groups = {}

    for event in parents:
        root = find(
            event
        )

        groups.setdefault(
            root,
            [],
        ).append(
            event
        )

    equivalence_groups = []

    for aliases in groups.values():
        aliases = sorted(
            set(aliases)
        )

        if len(aliases) < 2:
            continue

        equivalence_groups.append(
            {
                "canonical_event": (
                    aliases[0]
                ),
                "aliases": aliases,
            }
        )

    return {
        "equivalence_groups": (
            equivalence_groups
        ),
        "pairwise_decisions": (
            decisions
        ),
    }


def resolve_event_aliases(
    sources,
    constraints,
    model=DEFAULT_MODEL,
):
    decisions = (
        adjudicate_event_pairs(
            sources,
            constraints,
            model=model,
        )
    )

    return _build_resolution(
        decisions
    )


def apply_event_resolution(
    constraints,
    resolution,
):
    alias_map = {}

    for group in resolution[
        "equivalence_groups"
    ]:
        canonical = group[
            "canonical_event"
        ]

        for alias in group[
            "aliases"
        ]:
            alias_map[
                alias
            ] = canonical

    normalized = []

    for constraint in constraints:
        item = dict(
            constraint
        )

        event = item.get(
            "event"
        )

        if event in alias_map:
            item["event"] = (
                alias_map[event]
            )

        ref = item.get(
            "ref"
        )

        if ref in alias_map:
            item["ref"] = (
                alias_map[ref]
            )

        normalized.append(
            item
        )

    return normalized