import unittest

from review_pirate import render, validate, validate_profile


class RenderTests(unittest.TestCase):
    def valid_base(self):
        return {
            "comparison": "test",
            "products": [{"id": "x", "name": "X"}],
            "sources": [
                {
                    "id": "a",
                    "title": "A",
                    "url": "https://example.com/a"
                }
            ],
            "claims": []
        }

    def test_conflict_is_visible(self):
        data = self.valid_base()
        data["sources"].append(
            {"id": "b", "title": "B", "url": "https://example.com/b"}
        )
        data["claims"] = [
            {
                "product_id": "x",
                "topic": "durability",
                "claim": "holds up well",
                "stance": "support",
                "evidence_type": "reported_experience",
                "source_id": "a",
                "confidence": 0.7
            },
            {
                "product_id": "x",
                "topic": "durability",
                "claim": "failed early",
                "stance": "oppose",
                "evidence_type": "reported_experience",
                "source_id": "b",
                "confidence": 0.5
            }
        ]

        output = render(data)
        self.assertIn("conflict detected", output)
        self.assertIn("holds up well", output)
        self.assertIn("failed early", output)

    def test_profile_surfaces_matching_product(self):
        data = self.valid_base()
        data["products"].append({"id": "y", "name": "Y"})
        data["decision_questions"] = [
            {
                "id": "outdoor",
                "prompt": "Need outdoor use?",
                "outcomes": [
                    {
                        "answer": True,
                        "label": "yes",
                        "product_id": "x",
                        "reason": "works outside"
                    },
                    {
                        "answer": False,
                        "label": "no",
                        "product_id": "y",
                        "reason": "simpler indoors"
                    }
                ]
            }
        ]

        output = render(data, {"outdoor": True})
        self.assertIn("For this buyer", output)
        self.assertIn("works outside", output)
        self.assertIn("because: Need outdoor use?", output)

    def test_unknown_profile_key_fails_validation(self):
        data = self.valid_base()
        data["decision_questions"] = []
        self.assertTrue(validate_profile(data, {"mystery": True}))

    def test_unknown_source_fails_validation(self):
        data = self.valid_base()
        data["claims"] = [
            {
                "product_id": "x",
                "topic": "durability",
                "claim": "claim",
                "stance": "support",
                "source_id": "missing"
            }
        ]
        self.assertTrue(validate(data))

    def test_confidence_must_be_bounded(self):
        data = self.valid_base()
        data["claims"] = [
            {
                "product_id": "x",
                "topic": "durability",
                "claim": "claim",
                "stance": "support",
                "source_id": "a",
                "confidence": 1.4
            }
        ]
        self.assertTrue(validate(data))

    def test_duplicate_source_ids_fail_validation(self):
        data = self.valid_base()
        data["sources"].append(
            {"id": "a", "title": "also A", "url": "https://example.com/also-a"}
        )
        self.assertTrue(validate(data))

    def test_profile_answers_must_be_boolean(self):
        data = self.valid_base()
        data["decision_questions"] = [
            {
                "id": "outdoor",
                "prompt": "Need outdoor use?",
                "outcomes": [
                    {
                        "answer": True,
                        "product_id": "x",
                        "reason": "works outside"
                    }
                ]
            }
        ]
        self.assertTrue(validate_profile(data, {"outdoor": "yes"}))


if __name__ == "__main__":
    unittest.main()
