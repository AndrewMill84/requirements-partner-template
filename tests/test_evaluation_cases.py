"""Dataset integrity only: these tests do not evaluate an AI response."""

import json
from pathlib import Path
import unittest


class EvaluationDataset(unittest.TestCase):
    def test_cases_have_unique_ids_inputs_and_observable_rubrics(self):
        path = Path(__file__).resolve().parents[1] / "evals/cases.json"
        self.assertTrue(path.exists(), "The behavioural evaluation dataset is missing")
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], 1)
        cases = data["cases"]
        self.assertGreaterEqual(len(cases), 6)
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        for case in cases:
            with self.subTest(case=case["id"]):
                for key in ["id", "title", "classification", "task"]:
                    self.assertIsInstance(case[key], str)
                    self.assertTrue(case[key].strip())
                for key in ["context", "must_do", "must_not_do", "critical_checks"]:
                    self.assertIsInstance(case[key], list)
                    self.assertTrue(case[key])
                    self.assertTrue(all(isinstance(item, str) and item.strip() for item in case[key]))
        classifications = {case["classification"] for case in cases}
        self.assertTrue({"confirmed-authority", "policy-conflict", "missing-financial-rule",
                         "engineering-choice", "scoped-readiness", "evidence-gap"}.issubset(classifications))


if __name__ == "__main__":
    unittest.main()
