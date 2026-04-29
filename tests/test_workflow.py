from src.workflow import RecommendationWorkflow


def test_workflow_returns_trace_and_recommendations():
    workflow = RecommendationWorkflow()
    songs = [
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
    user = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    }

    result = workflow.run(user, songs, k=2, mode="specialized", use_rag=True)

    assert result["mode"] == "specialized"
    assert result["recommendations"]
    assert any(log["step"] == "PLAN" for log in result["logs"])
    assert any(log["step"] == "RETRIEVE" for log in result["logs"])
    assert any(log["step"] == "REFLECT" for log in result["logs"])


def test_specialized_mode_returns_weights():
    workflow = RecommendationWorkflow()
    songs = [
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
    user = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    }

    result = workflow.run(user, songs, k=1, mode="specialized", use_rag=True)

    assert result["weights"] is not None
    assert result["weights"]["energy_max_points"] >= 1.5
