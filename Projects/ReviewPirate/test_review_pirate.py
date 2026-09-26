import unittest

from review_pirate import render


class RenderTests(unittest.TestCase):
    def test_conflict_is_visible(self):
        data = {
            "comparison": "test",
            "products": [{"id": "x", "name": "X"}],
            "sources": [
                {"id": "a", "title": "A", "url": "https://example.com/a"},
                {"id": "b", "title": "B", "url": "https://example.com/b"}
            ],
            "claims": [
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
        }

        output = render(data)
        self.assertIn("conflict detected", output)
        self.assertIn("holds up well", output)
        self.assertIn("failed early", output)


if __name__ == "__main__":
    unittest.main()
