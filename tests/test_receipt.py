import json
import unittest
from pathlib import Path

from src.reality_compiler.receipt import (
    render_html,
    render_markdown,
)


ROOT = Path(__file__).resolve().parents[1]


class DecisionReceiptTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(
            ROOT / "eval/cases_v0_3/case_04.json"
        ) as f:
            cls.case = json.load(f)

        cls.record = None

        with open(
            ROOT
            / "eval/results/model_backed_postfix_v0_1.jsonl"
        ) as f:
            for line in f:
                row = json.loads(line)

                if row["case_id"] == "case_04":
                    cls.record = row
                    break

        if cls.record is None:
            raise RuntimeError(
                "case_04 result not found"
            )

    def test_html_receipt_contains_decision(self):
        output = render_html(
            self.case,
            self.record,
        )

        self.assertIn(
            "NOT FEASIBLE",
            output,
        )

        self.assertIn(
            "MINIMAL VERIFIED REPAIR",
            output,
        )

        self.assertIn(
            "AFTER REPAIR: FEASIBLE — SAT",
            output,
        )

    def test_html_receipt_contains_evidence(self):
        output = render_html(
            self.case,
            self.record,
        )

        self.assertIn(
            "M1",
            output,
        )

        self.assertIn(
            "S1",
            output,
        )

        self.assertIn(
            "P1",
            output,
        )

        self.assertIn(
            "C1 · C2 · C4",
            output,
        )

    def test_receipt_contains_boundary_language(self):
        output = render_html(
            self.case,
            self.record,
        )

        self.assertIn(
            "Boundary-minimal",
            output,
        )

        self.assertIn(
            "Human decision required",
            output,
        )

    def test_markdown_receipt_renders(self):
        output = render_markdown(
            self.case,
            self.record,
        )

        self.assertIn(
            "NOT FEASIBLE",
            output,
        )

        self.assertIn(
            "Minimal Verified Repair",
            output,
        )


if __name__ == "__main__":
    unittest.main()