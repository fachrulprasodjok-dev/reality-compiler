import unittest

from src.reality_compiler.extractor import INSTRUCTIONS


class ExtractorContractTests(unittest.TestCase):

    def test_same_event_is_explicitly_defined(self):
        self.assertIn(
            "6. same_event",
            INSTRUCTIONS,
        )

    def test_constitutive_relationship_is_covered(self):
        self.assertIn(
            "constitutes",
            INSTRUCTIONS.lower(),
        )

    def test_same_event_requires_explicit_identity(self):
        self.assertIn(
            "Do not use same_event",
            INSTRUCTIONS,
        )


if __name__ == "__main__":
    unittest.main()