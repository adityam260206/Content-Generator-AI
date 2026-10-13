"""Protocol for larger randomized follow-up experiments and measurable evaluation criteria."""

from typing import Any, Dict


def get_experimental_protocol() -> Dict[str, Any]:
    """Return the detailed experimental protocol for follow-up validation."""
    return {
        "title": "Large-Scale Randomized Controlled Evaluation of LLM Verification Pipelines in Higher Education",
        "study_design": {
            "type": "3x3 Factorial Randomized Block Design",
            "independent_variables": [
                {
                    "name": "Strategy",
                    "levels": ["Full Context", "Retrieval-Augmented", "GenerateVerify"]
                },
                {
                    "name": "Discipline Domain",
                    "levels": ["STEM (Computer Systems)", "Social Sciences (Macroeconomics)", "Life Sciences (Molecular Biology)"]
                },
                {
                    "name": "Target Cognitive Level",
                    "levels": ["Lower-Order (Remember/Understand)", "Mid-Order (Apply)", "Higher-Order (Analyze/Evaluate)"]
                }
            ],
            "sample_size_calculation": {
                "total_questions": 360,
                "questions_per_cell": 40,
                "power": 0.85,
                "significance_alpha": 0.05,
                "minimal_detectable_effect_size_d": 0.42
            }
        },
        "evaluation_panel_and_blinded_rubric": {
            "evaluator_panel": "12 independent domain-expert university professors and teaching assistants",
            "blinding_protocol": "Double-blinded: Question stems, distractors, and keys presented without generation metadata or strategy labels in randomized sequence order.",
            "inter_rater_reliability": {
                "primary_metric": "Cohen's Quadratic Weighted Kappa (kappa >= 0.82 target)",
                "multi_rater_metric": "Fleiss' Kappa across expert panels",
                "consensus_resolution": "Delphi reconciliation panel for items with kappa discrepancy > 1.0"
            }
        },
        "measurable_evaluation_criteria": [
            {
                "criterion": "Strict Grounding Rate (SGR)",
                "operational_definition": "Binary measure (1/0): Every factual premise in question stem and the single correct answer must be explicitly verifiable from verbatim source text span.",
                "target_threshold": "GenerateVerify >= 98.0%, Baseline >= 80.0%"
            },
            {
                "criterion": "Distractor Non-Plausibility vs Factuality Balance",
                "operational_definition": "Distractors must be domain-plausible misconceptions yet demonstrably refuted by source material.",
                "target_threshold": "Distractor Validity Index >= 0.90"
            },
            {
                "criterion": "Cognitive Complexity Index (CCI)",
                "operational_definition": "Bloom's Revised Taxonomy indexed rating (1.00 to 1.50 scale).",
                "target_threshold": "GenerateVerify CCI >= 1.250"
            },
            {
                "criterion": "Linguistic Ambiguity & Clarity Index",
                "operational_definition": "Absence of negative phrasing, unfocused stems, or double-barrelled questions.",
                "target_threshold": "Clarity Index >= 95%"
            },
            {
                "criterion": "Student Learning Gain (Empirical Pilot)",
                "operational_definition": "Normalized learning gain g = (Score_post - Score_pre) / (100 - Score_pre) across student cohorts.",
                "target_threshold": "Statistically significant improvement in post-test mastery (p < 0.01)"
            }
        ]
    }
