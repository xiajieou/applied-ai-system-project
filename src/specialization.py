"""Specialized recommendation weight profiles.

The project uses this module to demonstrate a constrained, specialized mode
that behaves differently from the baseline scoring setup without changing the
core recommender algorithm.
"""

from __future__ import annotations

from typing import Any, Dict

from src.recommender import _merged_weights, _parse_float


def build_specialized_weights(
    user_prefs: Dict[str, Any],
    base_weights: Dict[str, float] | None = None,
) -> Dict[str, float]:
    """Return lightly tuned weights for a specialized recommendation profile."""

    weights = _merged_weights(base_weights)
    target_energy = _parse_float(user_prefs.get("target_energy", user_prefs.get("energy", 0.0)))
    likes_acoustic = bool(user_prefs.get("likes_acoustic", False))
    favorite_mood = str(user_prefs.get("favorite_mood", user_prefs.get("mood", ""))).strip().lower()
    favorite_genre = str(user_prefs.get("favorite_genre", user_prefs.get("genre", ""))).strip().lower()

    if target_energy >= 0.8:
        weights["energy_max_points"] += 0.25
        weights["energy_penalty_factor"] += 0.10
    elif target_energy <= 0.45:
        weights["energy_max_points"] += 0.10
        weights["energy_penalty_factor"] = max(1.5, weights["energy_penalty_factor"] - 0.35)

    if likes_acoustic:
        weights["acoustic_high_bonus"] += 0.15
    else:
        weights["acoustic_low_bonus"] += 0.10

    if favorite_mood in {"chill", "peaceful", "calm"}:
        weights["mood_weight"] += 0.25
        weights["energy_penalty_factor"] = max(1.5, weights["energy_penalty_factor"] - 0.15)

    if favorite_genre in {"rock", "lofi", "pop"}:
        weights["genre_weight"] += 0.10

    return weights
