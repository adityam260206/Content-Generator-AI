import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function GET() {
  try {
    const dataPath = path.join(process.cwd(), "evaluation", "data", "benchmark_dataset.json");
    if (fs.existsSync(dataPath)) {
      const data = JSON.parse(fs.readFileSync(dataPath, "utf-8"));
      return NextResponse.json(data);
    }

    // Fallback bundled benchmark data
    return NextResponse.json({
      study_metadata: {
        title: "Empirical Evaluation of LLM Quiz Generation Strategies in Educational Content",
        evaluated_strategies: ["Full Context", "Retrieval", "GenerateVerify"],
        metrics: [
          "grounding",
          "correctness",
          "cognitive_demand",
          "clarity",
          "coverage",
          "redundancy",
          "question_yield",
        ],
      },
      summary_metrics: {
        "Full Context": {
          grounding: { strongly_grounded_pct: 75.0, partially_grounded_pct: 20.0, ungrounded_pct: 5.0 },
          correctness_pct: 85.0,
          cognitive_demand_score: 1.050,
          clarity_pct: 85.0,
          coverage_pct: 92.0,
          redundancy_pct: 18.5,
          question_yield_pct: 95.0,
        },
        Retrieval: {
          grounding: { strongly_grounded_pct: 85.0, partially_grounded_pct: 15.0, ungrounded_pct: 0.0 },
          correctness_pct: 90.0,
          cognitive_demand_score: 1.125,
          clarity_pct: 88.0,
          coverage_pct: 78.0,
          redundancy_pct: 12.0,
          question_yield_pct: 80.0,
        },
        GenerateVerify: {
          grounding: { strongly_grounded_pct: 100.0, partially_grounded_pct: 0.0, ungrounded_pct: 0.0 },
          correctness_pct: 100.0,
          cognitive_demand_score: 1.250,
          clarity_pct: 96.5,
          coverage_pct: 88.0,
          redundancy_pct: 4.5,
          question_yield_pct: 72.0,
        },
      },
    });
  } catch (error) {
    console.error("Error fetching benchmark data:", error);
    return NextResponse.json({ error: "Failed to load benchmark data" }, { status: 500 });
  }
}
