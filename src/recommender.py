from __future__ import annotations

from typing import Any, Dict, List, Tuple
from dataclasses import dataclass
import csv


DEFAULT_WEIGHTS: Dict[str, float] = {
    "genre_weight": 2.0,
    "mood_weight": 1.0,
    "energy_max_points": 1.5,
    "energy_penalty_factor": 2.5,
    "acoustic_high_bonus": 0.5,
    "acoustic_low_bonus": 0.2,
}


def _parse_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _song_from_dict(song_data: Dict[str, Any]) -> Song:
    return Song(
        id=int(song_data.get("id", 0)),
        title=str(song_data.get("title", "")),
        artist=str(song_data.get("artist", "")),
        genre=str(song_data.get("genre", "")).strip().lower(),
        mood=str(song_data.get("mood", "")).strip().lower(),
        energy=_parse_float(song_data.get("energy", 0.0)),
        tempo_bpm=_parse_float(song_data.get("tempo_bpm", 0.0)),
        valence=_parse_float(song_data.get("valence", 0.0)),
        danceability=_parse_float(song_data.get("danceability", 0.0)),
        acousticness=_parse_float(song_data.get("acousticness", 0.0)),
    )


def _merged_weights(weights: Dict[str, float] | None = None) -> Dict[str, float]:
    merged = dict(DEFAULT_WEIGHTS)
    if weights:
        merged.update(weights)
    return merged


def _score_song_like(
    user_genre: str,
    user_mood: str,
    target_energy: float,
    likes_acoustic: bool,
    song: Song,
    weights: Dict[str, float] | None = None,
) -> Tuple[float, str]:
    w = _merged_weights(weights)
    score = 0.0
    reasons: List[str] = []

    if song.genre.strip().lower() == user_genre.strip().lower():
        score += w["genre_weight"]
        reasons.append(f"genre matches (+{w['genre_weight']:.2f})")

    if song.mood.strip().lower() == user_mood.strip().lower():
        score += w["mood_weight"]
        reasons.append(f"mood matches (+{w['mood_weight']:.2f})")

    energy_gap = abs(song.energy - target_energy)
    energy_points = max(0.0, w["energy_max_points"] - energy_gap * w["energy_penalty_factor"])
    score += energy_points
    reasons.append(f"energy is close ({energy_points:.2f} points)")

    acoustic_bonus = 0.0
    if likes_acoustic and song.acousticness >= 0.65:
        acoustic_bonus = w["acoustic_high_bonus"]
        score += acoustic_bonus
        reasons.append(f"fits acoustic preference (+{acoustic_bonus:.2f})")
    elif not likes_acoustic and song.acousticness <= 0.35:
        acoustic_bonus = w["acoustic_low_bonus"]
        score += acoustic_bonus
        reasons.append(f"matches low-acoustic preference (+{acoustic_bonus:.2f})")

    explanation = "; ".join(reasons) if reasons else "baseline score from feature similarity"
    return score, explanation


def score_song(
    user_prefs: Dict[str, Any],
    song: Dict[str, Any],
    weights: Dict[str, float] | None = None,
) -> Tuple[float, List[str]]:
    """Score one song against a user profile and return the score with reasons."""
    song_object = _song_from_dict(song)
    score, explanation = _score_song_from_prefs(user_prefs, song_object, weights)
    reasons = [part.strip() for part in explanation.split(";") if part.strip()]
    return score, reasons


def _score_song_from_prefs(
    user_prefs: Dict[str, Any],
    song: Song,
    weights: Dict[str, float] | None = None,
) -> Tuple[float, str]:
    return _score_song_like(
        str(user_prefs.get("favorite_genre", user_prefs.get("genre", ""))),
        str(user_prefs.get("favorite_mood", user_prefs.get("mood", ""))),
        _parse_float(user_prefs.get("target_energy", user_prefs.get("energy", 0.0))),
        bool(user_prefs.get("likes_acoustic", False)),
        song,
        weights,
    )

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked_songs = sorted(
            self.songs,
            key=lambda song: _score_song_like(
                user.favorite_genre,
                user.favorite_mood,
                user.target_energy,
                user.likes_acoustic,
                song,
            )[0],
            reverse=True,
        )
        return ranked_songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, explanation = _score_song_like(
            user.favorite_genre,
            user.favorite_mood,
            user.target_energy,
            user.likes_acoustic,
            song,
        )
        return f"Score {score:.2f}: {song.title} stands out because {explanation}."

def load_songs(csv_path: str) -> List[Dict[str, Any]]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict[str, Any]] = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            song: Dict[str, Any] = {
                "id": int(row.get("id", 0)),
                "title": row.get("title", ""),
                "artist": row.get("artist", ""),
                "genre": row.get("genre", "").strip().lower(),
                "mood": row.get("mood", "").strip().lower(),
                "energy": _parse_float(row.get("energy", 0.0)),
                "tempo_bpm": _parse_float(row.get("tempo_bpm", 0.0)),
                "valence": _parse_float(row.get("valence", 0.0)),
                "danceability": _parse_float(row.get("danceability", 0.0)),
                "acousticness": _parse_float(row.get("acousticness", 0.0)),
            }
            songs.append(song)
    return songs

def recommend_songs(
    user_prefs: Dict[str, Any],
    songs: List[Dict[str, Any]],
    k: int = 5,
    weights: Dict[str, float] | None = None,
) -> List[Tuple[Dict[str, Any], float, List[str]]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_results: List[Tuple[Dict[str, Any], float, List[str]]] = []

    for song_data in songs:
        score, reasons = score_song(user_prefs, song_data, weights)
        scored_results.append((song_data, score, reasons))

    scored_results.sort(key=lambda item: item[1], reverse=True)
    return scored_results[:k]
