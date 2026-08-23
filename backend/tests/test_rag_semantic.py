from backend.api.routes.chat import get_all_schemes
from backend.rag.vector_store import index_schemes, reset_index
from backend.rag.retriever import retrieve_relevant_schemes


def setup_rag():
    """
    Reset and rebuild the ChromaDB scheme index.
    """
    reset_index()

    schemes = get_all_schemes()

    if not schemes:
        raise RuntimeError("No schemes were loaded.")

    index_schemes(schemes)

    return schemes


def print_results(title, results):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    for position, result in enumerate(results, start=1):
        print(f"{position}. {result['name']}")
        print(f"   Category: {result['category']}")
        print(f"   Semantic Distance: {result['distance']}")
        print(f"   Keyword Boost: {result['keyword_boost']}")
        print(f"   Final Ranking Score: {result['ranking_score']}")
        print("-" * 50)


def test_farmer_query():
    schemes = setup_rag()

    query = (
        "I am a farmer and I need financial support "
        "for agriculture, farming and agricultural land."
    )

    results = retrieve_relevant_schemes(
        user_query=query,
        candidate_schemes=schemes,
        top_k=5
    )

    assert len(results) > 0

    print_results(
        "FARMER QUERY RESULTS",
        results
    )

    top_names = [
        result["name"].upper()
        for result in results[:3]
    ]

    assert any(
        "KISAN" in name or "RYTHU" in name
        for name in top_names
    )


def test_student_query():
    schemes = setup_rag()

    query = (
        "I am a student looking for scholarship and "
        "financial assistance for my higher education "
        "and college studies."
    )

    results = retrieve_relevant_schemes(
        user_query=query,
        candidate_schemes=schemes,
        top_k=5
    )

    assert len(results) > 0

    print_results(
        "STUDENT QUERY RESULTS",
        results
    )

    top_names = [
        result["name"].upper()
        for result in results[:3]
    ]

    assert any(
        "SCHOLARSHIP" in name
        or "VIDYA" in name
        for name in top_names
    )


def test_health_query():
    schemes = setup_rag()

    query = (
        "I need government health insurance and financial "
        "support for hospital treatment and medical expenses."
    )

    results = retrieve_relevant_schemes(
        user_query=query,
        candidate_schemes=schemes,
        top_k=5
    )

    assert len(results) > 0

    print_results(
        "HEALTHCARE QUERY RESULTS",
        results
    )

    # Ayushman Bharat should now be in the top 2.
    top_names = [
        result["name"].upper()
        for result in results[:2]
    ]

    assert any(
        "AYUSHMAN" in name
        for name in top_names
    )