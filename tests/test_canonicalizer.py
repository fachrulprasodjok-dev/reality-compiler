import unittest

from src.reality_compiler.canonicalizer import (
    canonicalize_constraints,
)


class CanonicalizerTests(unittest.TestCase):

    def test_same_event_merges_two_symbols(self):
        constraints = [
            {
                "id": "C1",
                "kind": "fixed_date",
                "event": "security_review",
                "date": "2026-10-16",
                "source_id": "S1",
                "description": "Security review completes Oct 16.",
            },
            {
                "id": "C2",
                "kind": "same_event",
                "event": "security_review",
                "ref": "security_approval",
                "source_id": "P1",
                "description": (
                    "Security review completion "
                    "constitutes security approval."
                ),
            },
            {
                "id": "C3",
                "kind": "before_or_same",
                "event": "security_approval",
                "ref": "release",
                "source_id": "P1",
                "description": (
                    "Security approval must complete "
                    "by release."
                ),
            },
        ]

        result = canonicalize_constraints(
            constraints
        )

        self.assertEqual(
            len(result),
            2,
        )

        self.assertEqual(
            result[0]["event"],
            "security_approval",
        )

        self.assertEqual(
            result[1]["event"],
            "security_approval",
        )

    def test_same_event_constraint_is_removed(self):
        constraints = [
            {
                "id": "C1",
                "kind": "same_event",
                "event": "a",
                "ref": "b",
                "source_id": "P1",
                "description": "A is the same event as B.",
            }
        ]

        result = canonicalize_constraints(
            constraints
        )

        self.assertEqual(
            result,
            [],
        )

    def test_chained_same_event_relations_merge(self):
        constraints = [
            {
                "id": "C1",
                "kind": "same_event",
                "event": "alpha",
                "ref": "beta",
                "source_id": "P1",
                "description": "Alpha is Beta.",
            },
            {
                "id": "C2",
                "kind": "same_event",
                "event": "beta",
                "ref": "gamma",
                "source_id": "P2",
                "description": "Beta is Gamma.",
            },
            {
                "id": "C3",
                "kind": "deadline",
                "event": "gamma",
                "date": "2026-10-15",
                "source_id": "M1",
                "description": "Gamma deadline.",
            },
        ]

        result = canonicalize_constraints(
            constraints
        )

        self.assertEqual(
            result[0]["event"],
            "alpha",
        )


if __name__ == "__main__":
    unittest.main()