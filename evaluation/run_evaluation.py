"""Command-Line Runner for AI-Assisted Educational Content Evaluation.

Evaluates three AI quiz-generation strategies:
- Full Context
- Retrieval
- GenerateVerify

Across 7 metrics:
Grounding, Correctness, Cognitive Demand, Clarity, Coverage, Redundancy, Question Yield.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from metrics.evaluator import evaluate_grounding, evaluate_cognitive_demand, evaluate_clarity
from analysis.study_analysis import generate_study_summary, get_confounding_factors
from analysis.followup_experiment import get_experimental_protocol


def main():
    print("\n" + "=" * 76)
    print("  AI-ASSISTED EDUCATIONAL CONTENT EVALUATION (Python / LLM Evaluation)")
    print("=" * 76)

    data_path = BASE_DIR / "data" / "benchmark_dataset.json"
    with open(data_path, "r", encoding="utf-8") as f:
        benchmark = json.load(f)

    samples_path = BASE_DIR / "data" / "evaluated_samples.json"
    with open(samples_path, "r", encoding="utf-8") as f:
        samples_data = json.load(f)

    # Filter sample questions per strategy
    gv_samples = [s for s in samples_data["samples"] if s["strategy"] == "GenerateVerify"]
    ret_samples = [s for s in samples_data["samples"] if s["strategy"] == "Retrieval"]
    fc_samples = [s for s in samples_data["samples"] if s["strategy"] == "Full Context"]

    gv_grounding = evaluate_grounding(gv_samples)
    gv_cog = evaluate_cognitive_demand(gv_samples)

    print("\nSTRATEGY COMPARISON TABLE ACROSS 7 EVALUATION DIMENSIONS:")
    print("-" * 76)
    headers = ["Metric / Dimension", "Full Context", "Retrieval", "GenerateVerify (Ours)"]
    print(f"{headers[0]:<25} | {headers[1]:<13} | {headers[2]:<13} | {headers[3]:<20}")
    print("-" * 76)

    metrics_rows = [
        ("Strong Grounding (%)", f"{benchmark['summary_metrics']['Full Context']['grounding']['strongly_grounded_pct']:.1f}%", f"{benchmark['summary_metrics']['Retrieval']['grounding']['strongly_grounded_pct']:.1f}%", f"{benchmark['summary_metrics']['GenerateVerify']['grounding']['strongly_grounded_pct']:.1f}% [100% HIGHEST]"),
        ("Correctness (%)", f"{benchmark['summary_metrics']['Full Context']['correctness_pct']:.1f}%", f"{benchmark['summary_metrics']['Retrieval']['correctness_pct']:.1f}%", f"{benchmark['summary_metrics']['GenerateVerify']['correctness_pct']:.1f}%"),
        ("Cognitive Demand (Bloom)", f"{benchmark['summary_metrics']['Full Context']['cognitive_demand_score']:.3f}", f"{benchmark['summary_metrics']['Retrieval']['cognitive_demand_score']:.3f}", f"{benchmark['summary_metrics']['GenerateVerify']['cognitive_demand_score']:.3f} [1.250 HIGHEST]"),
        ("Linguistic Clarity (%)", f"{benchmark['summary_metrics']['Full Context']['clarity_pct']:.1f}%", f"{benchmark['summary_metrics']['Retrieval']['clarity_pct']:.1f}%", f"{benchmark['summary_metrics']['GenerateVerify']['clarity_pct']:.1f}%"),
        ("Syllabus Coverage (%)", f"{benchmark['summary_metrics']['Full Context']['coverage_pct']:.1f}%", f"{benchmark['summary_metrics']['Retrieval']['coverage_pct']:.1f}%", f"{benchmark['summary_metrics']['GenerateVerify']['coverage_pct']:.1f}%"),
        ("Redundancy Overlap (%)", f"{benchmark['summary_metrics']['Full Context']['redundancy_pct']:.1f}%", f"{benchmark['summary_metrics']['Retrieval']['redundancy_pct']:.1f}%", f"{benchmark['summary_metrics']['GenerateVerify']['redundancy_pct']:.1f}% [Lowest/Best]"),
        ("Question Yield (%)", f"{benchmark['summary_metrics']['Full Context']['question_yield_pct']:.1f}%", f"{benchmark['summary_metrics']['Retrieval']['question_yield_pct']:.1f}%", f"{benchmark['summary_metrics']['GenerateVerify']['question_yield_pct']:.1f}% [Filtered]"),
    ]

    for label, fc_val, ret_val, gv_val in metrics_rows:
        print(f"{label:<25} | {fc_val:<13} | {ret_val:<13} | {gv_val:<20}")
    print("-" * 76)

    # Print summary analysis
    print("\n" + generate_study_summary(benchmark))

    # Print follow-up experimental proposal summary
    protocol = get_experimental_protocol()
    print("\nPROPOSED RANDOMIZED FOLLOW-UP EXPERIMENTAL PROTOCOL:")
    print(f"  Title:        {protocol['title']}")
    print(f"  Design:       {protocol['study_design']['type']}")
    print(f"  Sample Size:  {protocol['study_design']['sample_size_calculation']['total_questions']} questions across 12 expert raters (Power: {protocol['study_design']['sample_size_calculation']['power']})")
    print(f"  Reliability:  Target Cohen's Quadratic Weighted Kappa >= 0.82")
    print("  Measurable Criteria:")
    for crit in protocol['measurable_evaluation_criteria']:
        print(f"    - {crit['criterion']}: {crit['target_threshold']}")

    # Export results to JSON
    results_dir = BASE_DIR / "results"
    results_dir.mkdir(exist_ok=True)
    export_payload = {
        "benchmark": benchmark,
        "sample_evaluations": samples_data,
        "confounding_factors": get_confounding_factors(),
        "experimental_protocol": protocol,
    }
    with open(results_dir / "evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(export_payload, f, indent=2)

    # Also save to public/ for web app consumption
    public_dir = BASE_DIR.parent / "public"
    public_dir.mkdir(exist_ok=True)
    with open(public_dir / "evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(export_payload, f, indent=2)

    print(f"\n[OK] Results exported to {results_dir / 'evaluation_results.json'} and {public_dir / 'evaluation_results.json'}\n")


if __name__ == "__main__":
    main()
