"""Test suite for AI-Assisted Educational Content Evaluation.

Verifies:
1. GenerateVerify achieved 100% strongly grounded questions on the evaluated sample.
2. GenerateVerify achieved the highest cognitive-demand score of 1.250.
3. All 7 evaluation dimensions are computed for Full Context, Retrieval, and GenerateVerify.
4. Confounding factors and randomized follow-up experiments are properly structured.
"""

import json
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

from metrics.evaluator import evaluate_grounding, evaluate_cognitive_demand, evaluate_clarity
from analysis.study_analysis import get_confounding_factors
from analysis.followup_experiment import get_experimental_protocol


class TestEducationalEvaluation(unittest.TestCase):
    def setUp(self):
        data_path = BASE_DIR / "data" / "benchmark_dataset.json"
        with open(data_path, "r", encoding="utf-8") as f:
            self.benchmark = json.load(f)

        samples_path = BASE_DIR / "data" / "evaluated_samples.json"
        with open(samples_path, "r", encoding="utf-8") as f:
            self.samples_data = json.load(f)

    def test_generate_verify_achieved_100_percent_strongly_grounded(self):
        """Verify GenerateVerify achieved 100% strongly grounded questions on evaluated sample."""
        gv_samples = [s for s in self.samples_data["samples"] if s["strategy"] == "GenerateVerify"]
        self.assertGreater(len(gv_samples), 0)

        grounding = evaluate_grounding(gv_samples)
        self.assertEqual(
            grounding["strongly_grounded_pct"],
            100.0,
            f"GenerateVerify strongly grounded percentage should be 100%, got {grounding['strongly_grounded_pct']}%"
        )
        self.assertEqual(grounding["partially_grounded_pct"], 0.0)
        self.assertEqual(grounding["ungrounded_pct"], 0.0)

    def test_generate_verify_achieved_highest_cognitive_demand_1_250(self):
        """Verify GenerateVerify achieved the highest cognitive-demand score of 1.250."""
        gv_samples = [s for s in self.samples_data["samples"] if s["strategy"] == "GenerateVerify"]
        fc_samples = [s for s in self.samples_data["samples"] if s["strategy"] == "Full Context"]
        ret_samples = [s for s in self.samples_data["samples"] if s["strategy"] == "Retrieval"]

        gv_score = evaluate_cognitive_demand(gv_samples)
        fc_score = evaluate_cognitive_demand(fc_samples)
        ret_score = evaluate_cognitive_demand(ret_samples)

        # Assert GenerateVerify cognitive score is 1.250 on the sample
        self.assertEqual(
            gv_score,
            1.250,
            f"Expected cognitive score of 1.250, got {gv_score}"
        )
        # Assert it is higher than both baseline strategies
        self.assertGreater(gv_score, fc_score)
        self.assertGreater(gv_score, ret_score)

    def test_seven_evaluation_metrics_present_for_all_three_strategies(self):
        """Verify all three strategies are evaluated across all 7 dimensions."""
        required_metrics = [
            "grounding",
            "correctness_pct",
            "cognitive_demand_score",
            "clarity_pct",
            "coverage_pct",
            "redundancy_pct",
            "question_yield_pct",
        ]
        strategies = ["Full Context", "Retrieval", "GenerateVerify"]

        for strat in strategies:
            strat_metrics = self.benchmark["summary_metrics"][strat]
            for metric in required_metrics:
                self.assertIn(metric, strat_metrics, f"Missing metric {metric} in strategy {strat}")

    def test_confounding_factors_identified(self):
        """Verify confounding factors analysis is complete and documented."""
        factors = get_confounding_factors()
        self.assertGreaterEqual(len(factors), 4)
        factor_names = [f["factor"] for f in factors]
        self.assertTrue(any("Attention" in name or "Lost-in-the-Middle" in name for name in factor_names))
        self.assertTrue(any("Chunk Boundary" in name for name in factor_names))
        self.assertTrue(any("Pre-training" in name or "Domain Familiarity" in name for name in factor_names))

    def test_followup_experiment_protocol_measurable_criteria(self):
        """Verify proposed randomized follow-up experiments and measurable criteria."""
        protocol = get_experimental_protocol()
        self.assertIn("3x3 Factorial", protocol["study_design"]["type"])
        self.assertGreaterEqual(protocol["study_design"]["sample_size_calculation"]["total_questions"], 300)
        self.assertGreater(len(protocol["measurable_evaluation_criteria"]), 3)


if __name__ == "__main__":
    unittest.main()
