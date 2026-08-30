import json
import unittest
from pathlib import Path

from src.reality_compiler.schemas import validate_constraints


ROOT = Path(__file__).resolve().parents[1]


class SchemaValidationTests(unittest.TestCase):

    def test_case_02_gold_constraints_are_valid(self):
        case_path = ROOT / "eval" / "cases" / "case_02.json"

        with open(case_path) as f:
            case = json.load(f)

        self.assertTrue(
            validate_constraints(case["gold_constraints"])
        )

    def test_invalid_constraint_kind_is_rejected(self):
        bad_constraints = [
            {
                "id": "C_BAD",
                "kind": "probably_delayed",
                "event": "launch",
                "source_id": "X1",
                "description": "vague AI guess",
            }
        ]

        with self.assertRaises(ValueError):
            validate_constraints(bad_constraints)

    def test_duplicate_constraint_id_is_rejected(self):
        duplicate_constraints = [
            {
                "id": "C1",
                "kind": "deadline",
                "event": "launch",
                "date": "2026-09-30",
                "source_id": "M1",
                "description": "Launch deadline",
            },
            {
                "id": "C1",
                "kind": "fixed_date",
                "event": "freeze",
                "date": "2026-09-25",
                "source_id": "J1",
                "description": "Code freeze",
            },
        ]

        with self.assertRaises(ValueError):
            validate_constraints(duplicate_constraints)
    def test_same_event_constraint_is_valid(self):
        constraints = [
            {
                "id": "C1",
                "kind": "same_event",
                "event": "security_review",
                "ref": "security_approval",
                "source_id": "P1",
                "description": (
                    "Completing the security review "
                    "constitutes security approval."
                ),
            }
        ]

        self.assertTrue(
            validate_constraints(constraints)
        )

    def test_same_event_without_ref_is_rejected(self):
        constraints = [
            {
                "id": "C1",
                "kind": "same_event",
                "event": "security_review",
                "source_id": "P1",
                "description": (
                    "Completing the security review "
                    "constitutes security approval."
                ),
            }
        ]

        with self.assertRaises(ValueError):
            validate_constraints(constraints)

if __name__ == "__main__":
    unittest.main()