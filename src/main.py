"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from typing import Any, Dict, List, Tuple

from src.recommender import load_songs
from src.workflow import RecommendationWorkflow


def _print_recommendations(
    profile_name: str,
    profile: Dict[str, Any],
    songs: List[Dict[str, Any]],
    k: int = 5,
    weights: Dict[str, float] | None = None,
    mode: str = "baseline",
    use_rag: bool = True,
) -> List[Tuple[Dict[str, Any], float, List[str]]]:
    workflow = RecommendationWorkflow()
    result = workflow.run(profile, songs, k=k, mode=mode, use_rag=use_rag, weights=weights)
    recommendations = result["recommendations"]

    print(f"\n=== {profile_name} ===")
    for entry in result["logs"]:
        print(f"[{entry['step']}] {entry['message']}")

    for index, rec in enumerate(recommendations, start=1):
        song, score, reasons = rec
        reasons_text = "; ".join(reasons)
        print(f"{index}. {song['title']} - Score: {score:.2f}")
        print(f"   Reasons: {reasons_text}")
    return recommendations


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles: List[Tuple[str, Dict[str, Any]]] = [
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

    print("\nTop recommendations by profile:")
    baseline_results: Dict[str, List[Tuple[Dict[str, Any], float, List[str]]]] = {}
    for profile_name, profile in profiles:
        baseline_results[profile_name] = _print_recommendations(profile_name, profile, songs, k=5, mode="baseline", use_rag=True)

    print("\n=== Sensitivity Experiment: Weight Shift ===")
    print("Applied change: halve genre weight, double max energy contribution")

    shifted_weights = {
        "genre_weight": 1.0,
        "mood_weight": 1.0,
        "energy_max_points": 3.0,
        "energy_penalty_factor": 2.5,
        "acoustic_high_bonus": 0.5,
        "acoustic_low_bonus": 0.2,
    }

    target_profile_name, target_profile = profiles[0]
    shifted = _print_recommendations(
        f"{target_profile_name} (Weight-Shifted)",
        target_profile,
        songs,
        k=5,
        weights=shifted_weights,
        mode="specialized",
        use_rag=True,
    )

    baseline_titles = [song[0]["title"] for song in baseline_results[target_profile_name][:3]]
    shifted_titles = [song[0]["title"] for song in shifted[:3]]
    print("\nTop-3 comparison for High-Energy Pop:")
    print(f"Baseline: {baseline_titles}")
    print(f"Weight-shifted: {shifted_titles}")


if __name__ == "__main__":
    main()
