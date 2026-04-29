from src.evaluation import run_evaluation, summarize_evaluation


def test_evaluation_returns_rows_and_summary():
    results = run_evaluation()
    summary = summarize_evaluation(results)

    assert results["profiles_tested"] == 3
    assert len(results["rows"]) == 3
    assert "Profiles tested" in summary
    assert "RAG improved or matched" in summary
    assert "Specialized mode changed" in summary
