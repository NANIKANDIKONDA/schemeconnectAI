from backend.services.data_validator import load_and_validate_schemes
from backend.rag.vector_store import index_schemes, reset_index


def rebuild_scheme_index():
    """
    Validate schemes.json and rebuild the ChromaDB vector index.
    """

    print("\n" + "=" * 70)
    print("SCHEMECONNECT AI - RAG INDEX BUILDER")
    print("=" * 70)

    print("\nStep 1: Loading and validating schemes...")

    schemes, errors = load_and_validate_schemes()

    if errors:
        print("\nDataset contains validation errors.")
        print("Fix the errors before rebuilding the RAG index.\n")

        for error in errors:
            print(
                f"Index {error['index']} | "
                f"Scheme ID: {error['scheme_id']}"
            )
            print(
                f"Error: {error['error']}"
            )
            print("-" * 50)

        return False

    print(
        f"Validation successful. "
        f"{len(schemes)} schemes are ready."
    )

    print("\nStep 2: Removing old vector index...")

    reset_index()

    print("Old vector index removed.")

    print("\nStep 3: Creating embeddings and indexing schemes...")

    index_schemes(schemes)

    print(
        f"\nSuccessfully indexed {len(schemes)} schemes."
    )

    print("\nRAG index rebuild completed successfully.")

    print("=" * 70)

    return True


if __name__ == "__main__":
    rebuild_scheme_index()