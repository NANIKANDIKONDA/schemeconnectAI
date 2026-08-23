from backend.rag.retriever import retrieve_relevant_schemes


def print_results(title, results):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    if not results:
        print("No results found.")
        return

    for scheme in results:
        print(f"\nScheme: {scheme['name']}")
        print(f"Category: {scheme['category']}")
        print(f"Best Distance: {scheme['best_distance']:.4f}")

        print("\nRetrieved Chunks:")

        for chunk in scheme["chunks"]:
            print("-" * 50)
            print(f"Chunk ID: {chunk['chunk_id']}")
            print(f"Chunk Index: {chunk['chunk_index']}")
            print(f"Distance: {chunk['distance']:.4f}")
            print("\nContent:")
            print(chunk["content"])


def test_documents_retrieval():
    query = "What documents are required for PM-KISAN?"

    results = retrieve_relevant_schemes(
        user_query=query,
        top_k=5
    )

    print_results(
        "TEST 1: DOCUMENTS RETRIEVAL",
        results
    )

    assert results
    assert any(
        "PM-KISAN" in scheme["name"]
        for scheme in results
    )


def test_application_retrieval():
    query = "How can I apply for PM-KISAN?"

    results = retrieve_relevant_schemes(
        user_query=query,
        top_k=5
    )

    print_results(
        "TEST 2: APPLICATION RETRIEVAL",
        results
    )

    assert results


def test_benefits_retrieval():
    query = "What financial benefits does PM-KISAN provide?"

    results = retrieve_relevant_schemes(
        user_query=query,
        top_k=5
    )

    print_results(
        "TEST 3: BENEFITS RETRIEVAL",
        results
    )

    assert results