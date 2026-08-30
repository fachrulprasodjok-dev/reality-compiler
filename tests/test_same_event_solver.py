import unittest

from src.reality_compiler.solver import solve


class SameEventSolverIntegrationTests(unittest.TestCase):

    def test_same_event_can_expose_hidden_conflict(self):
        constraints = [
            {
                "id": "C1",
                "kind": "deadline",
                "event": "release",
                "date": "2026-10-15",
                "source_id": "M1",
                "description": "Release by Oct 15",
            },
            {
                "id": "C2",
                "kind": "fixed_date",
                "event": "security_review",
                "date": "2026-10-16",
                "source_id": "S1",
                "description": (
                    "Security review completes Oct 16"
                ),
            },
            {
                "id": "C3",
                "kind": "same_event",
                "event": "security_review",
                "ref": "security_approval",
                "source_id": "P1",
                "description": (
                    "Review completion constitutes approval"
                ),
            },
            {
                "id": "C4",
                "kind": "before_or_same",
                "event": "security_approval",
                "ref": "release",
                "source_id": "P1",
                "description": (
                    "Security approval complete by release"
                ),
            },
        ]

        result = solve(constraints)

        self.assertEqual(
            result.status,
            "UNSAT",
        )

        self.assertEqual(
            set(result.unsat_core),
            {"C1", "C2", "C4"},
        )


if __name__ == "__main__":
    unittest.main()