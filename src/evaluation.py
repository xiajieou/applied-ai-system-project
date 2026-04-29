"""Evaluation harness for the music recommender project.

This module compares baseline, RAG-enhanced, and specialized recommendation
mode behavior across a fixed set of demo user profiles. It prints concise
summary metrics so the project can document reliability and improvement claims.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from src.recommender import load_songs
from src.workflow import RecommendationWorkflow


DEMO_PROFILES: List[Tuple[str, Dict[str, Any]]] = [
    (
        "High-Energy Pop",
        {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.90,
            "likes_acoustic": False,
        },
    ),
    (
        "Chill Lofi",
        {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.35,
            "likes_acoustic": True,
        },
    ),
    (
        "Deep Intense Rock",
        {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.92,
            "likes_acoustic": False,
        },
    ),
]


def run_evaluation(csv_path: str = "data/songs.csv") -> Dict[str, Any]:
    """Run the evaluation suite and return machine-readable metrics."""

    songs = load_songs(csv_path)
    workflow = RecommendationWorkflow()

    rows: List[Dict[str, Any]] = []
    for profile_name, profile in DEMO_PROFILES:
        baseline = workflow.run(profile, songs, k=3, mode="baseline", use_rag=False)
        ragged = workflow.run(profile, songs, k=3, mode="baseline", use_rag=True)
        specialized = workflow.run(profile, songs, k=3, mode="specialized", use_rag=True)

        rows.append(
            {
                "profile": profile_name,
                "baseline_top_title": baseline["recommendations"][0][0]["title"],
                "rag_top_title": ragged["recommendations"][0][0]["title"],
                "specialized_top_title": specialized["recommendations"][0][0]["title"],
                "baseline_top_score": baseline["recommendations"][0][1],
                "rag_top_score": ragged["recommendations"][0][1],
                "specialized_top_score": specialized["recommendations"][0][1],
                "baseline_trace_len": len(baseline["logs"]),
                "rag_trace_len": len(ragged["logs"]),
                "specialized_trace_len": len(specialized["logs"]),
            }
        )

    return {
        "profiles_tested": len(rows),
        "rows": rows,
    }


def summarize_evaluation(results: Dict[str, Any]) -> str:
    """Convert evaluation results into a compact human-readable summary."""

    rows = results["rows"]
    rag_better_or_equal = sum(1 for row in rows if row["rag_top_score"] >= row["baseline_top_score"])
    specialized_changed_top = sum(1 for row in rows if row["specialized_top_title"] != row["baseline_top_title"])
    average_trace_len = sum(row["specialized_trace_len"] for row in rows) / max(1, len(rows))

    lines = [
        f"Profiles tested: {results['profiles_tested']}",
        f"RAG improved or matched the baseline top score in {rag_better_or_equal}/{len(rows)} profile(s).",
        f"Specialized mode changed the top recommendation in {specialized_changed_top}/{len(rows)} profile(s).",
        f"Average specialized trace length: {average_trace_len:.1f} steps.",
    ]
    return "\n".join(lines)


def main() -> None:
    """Run the evaluation harness and print the summary."""

    results = run_evaluation()
    print("=== Evaluation Summary ===")
    print(summarize_evaluation(results))

    for row in results["rows"]:
        print(f"\n[{row['profile']}]")
        print(f"Baseline:    {row['baseline_top_title']} ({row['baseline_top_score']:.2f})")
        print(f"RAG:         {row['rag_top_title']} ({row['rag_top_score']:.2f})")
        print(f"Specialized:  {row['specialized_top_title']} ({row['specialized_top_score']:.2f})")


if __name__ == "__main__":
    main()
