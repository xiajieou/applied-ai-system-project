"""Retrieval document loader for the music recommender RAG layer.

This module keeps the domain knowledge in a small, inspectable set of text
documents so the recommender can retrieve and inject relevant context before
ranking songs. The documents describe the scoring rules, feature meanings,
and a lightweight specialization guide.
"""

from __future__ import annotations

from typing import Dict, List


SONG_METADATA_GUIDE = """
SONG METADATA GUIDE
===================

Each song in the system has the following attributes:

1. genre (string): Primary musical genre.
   - Examples: pop, lofi, rock, ambient, jazz, synthwave, indie_pop
   - Usage: Matches against favorite_genre
   - Weight in scoring: 2.0 (high importance)

2. mood (string): Emotional tone of the song.
   - Examples: upbeat, chill, energetic, intense, melancholic, peaceful
   - Usage: Matches against favorite_mood
   - Weight in scoring: 1.0 (medium importance)

3. energy (float, 0.0-1.0): Overall energetic intensity.
   - 0.0 = very low (ambient, lo-fi, sleep music)
   - 1.0 = very high (intense rock, dance, metal)
   - Usage: Matched against target_energy with bonus for proximity
   - Max points: 1.5 (peaks at the target and decreases with distance)

4. acousticness (float, 0.0-1.0): Acoustic versus electronic balance.
   - 0.0 = pure electronic synthesis
   - 1.0 = pure acoustic instruments
   - Usage: Conditional bonus if the user likes acoustic music

5. tempo_bpm (integer): Beats per minute.
   - Range: 60-180 BPM typical
   - Usage: Context only; not directly scored

6. valence (float, 0.0-1.0): Musical positivity / happiness.
   - 0.0 = sad, dark, negative mood
   - 1.0 = happy, upbeat, positive mood
   - Usage: Context only; supports mood interpretation

7. danceability (float, 0.0-1.0): Rhythmic groove / beat clarity.
   - 0.0 = not danceable
   - 1.0 = highly danceable
   - Usage: Context only; supports genre interpretation
"""

USER_PREFERENCE_RULES = """
USER PREFERENCE RULES
=====================

The recommendation system uses four core user preference signals:

1. favorite_genre (string): Primary music taste.
   - Scoring rule: exact genre match = +2.0 points
   - Interpretation: genre is the strongest signal

2. favorite_mood (string): Preferred emotional tone.
   - Scoring rule: exact mood match = +1.0 points
   - Interpretation: mood helps refine the recommendation

3. target_energy (float, 0.0-1.0): Desired intensity level.
   - Scoring rule:
     * peak points (1.5) at exact target energy
     * decreases with distance: max(0, 1.5 - 2.5 * abs(song_energy - target_energy))
   - Interpretation: users have a sweet spot for activity level

4. likes_acoustic (boolean): Acoustic versus electronic preference.
   - Scoring rule:
     * if acousticness > 0.5: +0.5 bonus points
     * if acousticness <= 0.5: +0.2 bonus points
   - Interpretation: helps distinguish similar songs

COMBINING PREFERENCES:
- All scores are additive
- A song can score at most 5.0 points from these factors
- Top-k recommendations are selected by highest total score
"""

RECOMMENDATION_STRATEGY = """
RECOMMENDATION STRATEGY
=======================

The system uses a four-step ranking algorithm:

STEP 1: FEATURE SCORING
-----------------------
For each candidate song, calculate:
  - Genre score: 2.0 if genre matches favorite_genre
  - Mood score: 1.0 if mood matches favorite_mood
  - Energy score: max(0, 1.5 - 2.5 * abs(song.energy - target_energy))
  - Acoustic bonus: 0.5 if the user likes acoustic music and acousticness is high,
    otherwise 0.2 when the user prefers non-acoustic music and acousticness is low

STEP 2: AGGREGATION
-------------------
Sum all applicable scores for each song to get total_score.

STEP 3: RANKING
---------------
Sort songs by total_score in descending order.

STEP 4: SELECTION
-----------------
Return the top-k songs and include a human-readable explanation for each one.

EXPLANATION FORMAT
------------------
List which factors matched and how much each factor contributed.
"""

SPECIALIZATION_GUIDE = """
SPECIALIZATION GUIDE
====================

The system can operate in two modes:

BASELINE MODE:
- Uses the default weights and simple additive scoring
- Best for general-purpose recommendations and first-time users

SPECIALIZED MODE:
- Applies refined weight adjustments and context-aware preference rules
- Best for returning users or a more tailored demo

Specialization examples:
1. Mood context: shift energy weight when the profile suggests a mood need
2. History weighting: boost songs that match recent user taste patterns
3. Time context: adjust energy for time of day
4. Preference emphasis: slightly rebalance weights for specific audience styles
"""


class RAGDocumentLoader:
    """Load and serve retrieval documents for the recommender."""

    def __init__(self) -> None:
        self.documents: Dict[str, str] = {
            "song_metadata": SONG_METADATA_GUIDE.strip(),
            "user_preferences": USER_PREFERENCE_RULES.strip(),
            "recommendation_strategy": RECOMMENDATION_STRATEGY.strip(),
            "specialization": SPECIALIZATION_GUIDE.strip(),
        }
        self.metadata: Dict[str, Dict[str, int]] = {
            name: {
                "size_chars": len(content),
                "size_tokens": max(1, len(content) // 4),
                "sections": self._count_sections(content),
            }
            for name, content in self.documents.items()
        }

    @staticmethod
    def _count_sections(text: str) -> int:
        return sum(1 for line in text.splitlines() if line.strip().endswith("===="))

    def get_document(self, doc_name: str) -> str:
        if doc_name not in self.documents:
            raise KeyError(f"Unknown document: {doc_name}. Available: {sorted(self.documents)}")
        return self.documents[doc_name]

    def get_all_documents(self) -> Dict[str, str]:
        return dict(self.documents)

    def get_document_summary(self, doc_name: str) -> Dict[str, int]:
        if doc_name not in self.metadata:
            raise KeyError(f"Unknown document summary: {doc_name}")
        return dict(self.metadata[doc_name])

    def get_all_metadata(self) -> Dict[str, Dict[str, int]]:
        return {name: dict(meta) for name, meta in self.metadata.items()}

    def search_documents(self, keyword: str) -> Dict[str, List[str]]:
        keyword_lower = keyword.strip().lower()
        if not keyword_lower:
            return {}

        matches: Dict[str, List[str]] = {}
        for doc_name, content in self.documents.items():
            lines = [line.strip() for line in content.splitlines() if keyword_lower in line.lower().strip()]
            if lines:
                matches[doc_name] = lines
        return matches

    def build_context_prompt(self, sections: List[str] | None = None) -> str:
        if sections is None:
            sections = ["song_metadata", "user_preferences", "recommendation_strategy"]

        parts = ["# RAG CONTEXT: Domain Knowledge for Recommendations\n", "=" * 70, "\n\n"]
        for section in sections:
            parts.append(self.get_document(section))
            parts.append("\n\n")
        parts.append("=" * 70)
        parts.append("\n# END RAG CONTEXT\n")
        return "".join(parts)


_loader_instance: RAGDocumentLoader | None = None


def get_document_loader() -> RAGDocumentLoader:
    global _loader_instance
    if _loader_instance is None:
        _loader_instance = RAGDocumentLoader()
    return _loader_instance
