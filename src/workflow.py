"""Agentic workflow wrapper for the music recommender.

This module gives the project a visible multi-step trace: plan, retrieve,
score, verify, and reflect. The workflow is intentionally simple and safe,
but it demonstrates the structure required for an agentic system.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from src.recommender import recommend_songs
from src.retrieval.document_loader import get_document_loader
from src.specialization import build_specialized_weights


class RecommendationWorkflow:
    """Run the recommender with explicit observable steps."""

    def __init__(self) -> None:
        self.loader = get_document_loader()

    def run(
        self,
        user_prefs: Dict[str, Any],
        songs: List[Dict[str, Any]],
        k: int = 5,
        mode: str = "baseline",
        use_rag: bool = True,
        weights: Dict[str, float] | None = None,
    ) -> Dict[str, Any]:
        logs: List[Dict[str, str]] = []
        logs.append({"step": "PLAN", "message": f"Starting recommendation workflow in {mode} mode."})

        retrieval_sections = ["song_metadata", "user_preferences", "recommendation_strategy"]
        if mode == "specialized":
            retrieval_sections.append("specialization")

        context_prompt = ""
        if use_rag:
            context_prompt = self.loader.build_context_prompt(retrieval_sections)
            matches = self.loader.search_documents(str(user_prefs.get("favorite_genre", user_prefs.get("genre", ""))))
            logs.append(
                {
                    "step": "RETRIEVE",
                    "message": f"Retrieved {len(retrieval_sections)} context section(s) and {len(matches)} matched document(s).",
                }
            )
        else:
            logs.append({"step": "RETRIEVE", "message": "RAG disabled; using baseline scoring context."})

        weights = None
        if mode == "specialized":
            weights = build_specialized_weights(user_prefs, weights)
            logs.append({"step": "SPECIALIZE", "message": "Applied specialized weight profile for the current user."})
        elif weights is not None:
            logs.append({"step": "SPECIALIZE", "message": "Applied custom weight overrides for this run."})

        recommendations = recommend_songs(user_prefs, songs, k=k, weights=weights, use_rag=use_rag)
        logs.append({"step": "SCORE", "message": f"Ranked {len(songs)} song(s) and returned top {len(recommendations)}."})

        if recommendations:
            top_score = recommendations[0][1]
            bottom_score = recommendations[-1][1]
            spread = top_score - bottom_score
            logs.append({"step": "VERIFY", "message": f"Score spread from top to bottom recommendation was {spread:.2f}."})
        else:
            logs.append({"step": "VERIFY", "message": "No recommendations were produced."})

        if mode == "specialized":
            logs.append({"step": "REFLECT", "message": "Specialized mode emphasizes user context more strongly than the baseline."})
        else:
            logs.append({"step": "REFLECT", "message": "Baseline mode keeps the default scoring recipe unchanged."})

        return {
            "mode": mode,
            "context": context_prompt,
            "weights": weights,
            "recommendations": recommendations,
            "logs": logs,
        }
