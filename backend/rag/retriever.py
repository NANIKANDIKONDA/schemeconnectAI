from collections import defaultdict

from backend.rag.vector_store import get_collection
from backend.rag.embedder import embed_text


def retrieve_relevant_schemes(
    user_query: str,
    candidate_schemes: list = None,
    top_k: int = 10
) -> list[dict]:
    """
    Retrieve relevant chunks from ChromaDB.

    If candidate_schemes are provided, retrieval is restricted
    to those scheme IDs.

    The returned chunks are grouped by scheme.
    """

    collection = get_collection()

    # Convert user query into an embedding
    query_embedding = embed_text(user_query)

    where_filter = None

    # Restrict retrieval to candidate scheme IDs if provided
    if candidate_schemes:
        candidate_ids = [scheme.id for scheme in candidate_schemes]

        where_filter = {
            "scheme_id": {
                "$in": candidate_ids
            }
        }

    query_kwargs = {
        "query_embeddings": [query_embedding],
        "n_results": top_k
    }

    if where_filter:
        query_kwargs["where"] = where_filter

    # Query ChromaDB
    results = collection.query(**query_kwargs)

    if (
        not results
        or not results.get("ids")
        or not results["ids"]
        or not results["ids"][0]
    ):
        return []

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # Group retrieved chunks by original scheme
    grouped_schemes = defaultdict(
        lambda: {
            "id": None,
            "name": None,
            "category": None,
            "chunks": [],
            "best_distance": float("inf")
        }
    )

    for index, chunk_id in enumerate(ids):

        metadata = metadatas[index]
        scheme_id = metadata["scheme_id"]

        scheme = grouped_schemes[scheme_id]

        scheme["id"] = scheme_id
        scheme["name"] = metadata.get("name")
        scheme["category"] = metadata.get("category")

        distance = distances[index]

        scheme["chunks"].append({
            "chunk_id": chunk_id,
            "chunk_index": metadata.get("chunk_index"),
            "content": documents[index],
            "distance": distance
        })

        # Lower distance means better semantic match
        if distance < scheme["best_distance"]:
            scheme["best_distance"] = distance

    # Convert grouped dictionary to list
    retrieved_schemes = list(grouped_schemes.values())

    # Sort schemes using their best chunk distance
    retrieved_schemes.sort(
        key=lambda scheme: scheme["best_distance"]
    )

    return retrieved_schemes