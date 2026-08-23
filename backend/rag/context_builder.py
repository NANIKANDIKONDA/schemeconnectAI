from typing import List, Dict


def build_rag_context(retrieved_results: List[Dict]) -> str:
    """
    Convert retrieved ChromaDB chunks into clean context
    that can be passed to the LLM.

    Expected retrieved result structure:

    {
        "id": "...",
        "name": "...",
        "category": "...",
        "best_distance": 0.123,
        "chunks": [
            {
                "chunk_id": "...",
                "chunk_index": 1,
                "distance": 0.123,
                "content": "..."
            }
        ]
    }
    """

    if not retrieved_results:
        return "No relevant scheme information was retrieved."

    context_parts = []

    for scheme in retrieved_results:
        scheme_name = scheme.get("name", "Unknown Scheme")
        category = scheme.get("category", "Unknown Category")

        context_parts.append(
            f"\n{'=' * 60}\n"
            f"SCHEME: {scheme_name}\n"
            f"CATEGORY: {category}\n"
            f"{'=' * 60}"
        )

        chunks = scheme.get("chunks", [])

        for chunk in chunks:
            content = chunk.get("content", "").strip()

            if content:
                context_parts.append(content)

    return "\n\n".join(context_parts)