from src.retrieval.document_loader import get_document_loader


def test_document_loader_returns_core_documents():
    loader = get_document_loader()

    documents = loader.get_all_documents()

    assert "song_metadata" in documents
    assert "user_preferences" in documents
    assert "recommendation_strategy" in documents
    assert "specialization" in documents


def test_context_prompt_contains_expected_header():
    loader = get_document_loader()

    prompt = loader.build_context_prompt()

    assert "RAG CONTEXT" in prompt
    assert "SONG METADATA GUIDE" in prompt
    assert "USER PREFERENCE RULES" in prompt


def test_search_documents_finds_energy_guidance():
    loader = get_document_loader()

    matches = loader.search_documents("energy")

    assert matches
    assert any("energy" in line.lower() for lines in matches.values() for line in lines)
