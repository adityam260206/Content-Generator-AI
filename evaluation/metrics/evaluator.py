"""Metrics evaluator for educational content generation strategies.

Calculates the 7 evaluation dimensions specified in the study:
1. Grounding (Strongly Grounded %, Partially Grounded %, Ungrounded %)
2. Correctness (%)
3. Cognitive Demand (Bloom's Taxonomy Index)
4. Clarity (%)
5. Coverage (%)
6. Redundancy (% overlap)
7. Question Yield (%)
"""

from typing import Any, Dict, List


def evaluate_grounding(questions: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate the distribution of grounding across evaluated questions."""
    total = len(questions)
    if total == 0:
        return {"strongly_grounded_pct": 0.0, "partially_grounded_pct": 0.0, "ungrounded_pct": 0.0}

    strongly = sum(1 for q in questions if q.get("grounding_status") == "strongly_grounded")
    partially = sum(1 for q in questions if q.get("grounding_status") == "partially_grounded")
    ungrounded = sum(1 for q in questions if q.get("grounding_status") == "ungrounded")

    return {
        "strongly_grounded_pct": round((strongly / total) * 100, 2),
        "partially_grounded_pct": round((partially / total) * 100, 2),
        "ungrounded_pct": round((ungrounded / total) * 100, 2),
    }


def evaluate_cognitive_demand(questions: List[Dict[str, Any]]) -> float:
    """Calculate the mean cognitive demand score based on Bloom's taxonomy.
    
    Weights:
      Remember: 1.00
      Understand: 1.10
      Apply: 1.20
      Analyze: 1.30
      Evaluate/Create: 1.40
    """
    if not questions:
        return 0.0

    scores = []
    for q in questions:
        if "cognitive_score" in q:
            scores.append(float(q["cognitive_score"]))
        else:
            level = str(q.get("bloom_level", "")).lower()
            if "evaluate" in level or "create" in level:
                scores.append(1.40)
            elif "analyze" in level:
                scores.append(1.30)
            elif "apply" in level:
                scores.append(1.20)
            elif "understand" in level:
                scores.append(1.10)
            else:
                scores.append(1.00)

    mean_score = sum(scores) / len(scores)
    return round(mean_score, 3)


def evaluate_clarity(questions: List[Dict[str, Any]]) -> float:
    """Calculate linguistic clarity and unambiguous phrasing index (0-100%)."""
    if not questions:
        return 0.0
    clarity_values = [q.get("clarity_score", 0.85) * 100 for q in questions]
    return round(sum(clarity_values) / len(clarity_values), 2)


def evaluate_strategy_sample(
    strategy_name: str,
    questions: List[Dict[str, Any]],
    coverage_pct: float,
    redundancy_pct: float,
    question_yield_pct: float,
    correctness_pct: float,
) -> Dict[str, Any]:
    """Compile comprehensive evaluation report across all 7 dimensions for a strategy."""
    grounding = evaluate_grounding(questions)
    cognitive_demand = evaluate_cognitive_demand(questions)
    clarity = evaluate_clarity(questions)

    return {
        "strategy": strategy_name,
        "sample_size": len(questions),
        "grounding": grounding,
        "correctness_pct": correctness_pct,
        "cognitive_demand_score": cognitive_demand,
        "clarity_pct": clarity,
        "coverage_pct": coverage_pct,
        "redundancy_pct": redundancy_pct,
        "question_yield_pct": question_yield_pct,
    }
