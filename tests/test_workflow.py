from src.workflow import RecommendationWorkflow


def test_workflow_returns_trace_and_recommendations():
    workflow = RecommendationWorkflow()
    songs = [ # type: ignore
        {
            "id": 1,
            "title": "Bright Pop",
            "artist": "Test Artist",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9,
            "tempo_bpm": 120,
            "valence": 0.9,
            "danceability": 0.8,
            "acousticness": 0.2,
        },
        {
            "id": 2,
            "title": "Soft Lofi",
            "artist": "Test Artist",
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.4,
            "tempo_bpm": 80,
            "valence": 0.5,
            "danceability": 0.4,
            "acousticness": 0.9,
        },
    ]
    user = { # type: ignore
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    }

    result = workflow.run(user, songs, k=2, mode="specialized", use_rag=True) # type: ignore

    assert result["mode"] == "specialized"
    assert result["recommendations"]
    assert any(log["step"] == "PLAN" for log in result["logs"])
    assert any(log["step"] == "RETRIEVE" for log in result["logs"])
    assert any(log["step"] == "REFLECT" for log in result["logs"])


def test_specialized_mode_returns_weights():
    workflow = RecommendationWorkflow()
    songs = [ # type: ignore
        {
            "id": 1,
            "title": "Bright Pop",
            "artist": "Test Artist",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9,
            "tempo_bpm": 120,
            "valence": 0.9,
            "danceability": 0.8,
            "acousticness": 0.2,
        }
    ]
    user = { # type: ignore
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    }

    result = workflow.run(user, songs, k=1, mode="specialized", use_rag=True) # type: ignore

    assert result["weights"] is not None
    assert result["weights"]["energy_max_points"] >= 1.5


def test_custom_weight_overrides_are_preserved():
    workflow = RecommendationWorkflow()
    songs = [ # type: ignore
        {
            "id": 1,
            "title": "Bright Pop",
            "artist": "Test Artist",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9,
            "tempo_bpm": 120,
            "valence": 0.9,
            "danceability": 0.8,
            "acousticness": 0.2,
        }
    ]
    user = { # type: ignore
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    }
    custom_weights = {
        "genre_weight": 4.0,
        "mood_weight": 1.5,
    }

    result = workflow.run(user, songs, k=1, mode="baseline", use_rag=False, weights=custom_weights) # type: ignore

    assert result["weights"] == custom_weights
    assert result["recommendations"][0][1] > 0
