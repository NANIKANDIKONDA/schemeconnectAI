from backend.rag.query_builder import build_rag_query


def test_build_rag_query_with_profile():

    profile = {
        "age": 20,
        "state": "Andhra Pradesh",
        "occupation": "Farmer",
        "annual_income": 150000,
        "land_acres": 2,
        "education": None,
        "category": "General",
        "gender": None,
        "beneficiary_for": None,
        "user_intent": "Find agriculture schemes",
    }

    query = build_rag_query(
        user_message="What government schemes can I apply for?",
        profile=profile,
    )

    print("\n")
    print("=" * 70)
    print("PROFILE-AWARE RAG QUERY")
    print("=" * 70)
    print(query)
    print("=" * 70)

    assert "Andhra Pradesh" in query
    assert "Farmer" in query
    assert "150000" in query
    assert "2" in query
    assert "Find agriculture schemes" in query


def test_build_rag_query_without_profile():

    query = build_rag_query(
        user_message="Find government schemes for me",
        profile={},
    )

    print("\n")
    print("=" * 70)
    print("RAG QUERY WITHOUT PROFILE")
    print("=" * 70)
    print(query)
    print("=" * 70)

    assert "No additional profile information available." in query