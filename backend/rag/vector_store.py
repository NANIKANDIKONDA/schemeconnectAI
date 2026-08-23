import os

import chromadb
from dotenv import load_dotenv

from backend.rag.document_builder import build_document
from backend.rag.chunker import chunk_document
from backend.rag.embedder import embed_texts
from backend.models.scheme import Scheme


# Load environment variables from .env
load_dotenv()


_client = None


def get_chroma_client():
    """
    Create and reuse the Chroma Cloud client.
    """

    global _client

    if _client is None:

        api_key = os.getenv("CHROMA_API_KEY")
        tenant = os.getenv("CHROMA_TENANT")
        database = os.getenv("CHROMA_DATABASE")

        if not api_key:
            raise ValueError(
                "CHROMA_API_KEY is missing. "
                "Add it to your .env file."
            )

        if not tenant:
            raise ValueError(
                "CHROMA_TENANT is missing. "
                "Add it to your .env file."
            )

        if not database:
            raise ValueError(
                "CHROMA_DATABASE is missing. "
                "Add it to your .env file."
            )

        _client = chromadb.CloudClient(
            api_key=api_key,
            tenant=tenant,
            database=database
        )

        print(
            f"Connected to Chroma Cloud database: {database}"
        )

    return _client


def get_collection():
    """
    Get or create the schemes collection
    in Chroma Cloud.
    """

    client = get_chroma_client()

    return client.get_or_create_collection(
        name="schemes"
    )


def index_schemes(schemes: list[Scheme]):
    """
    Build documents, split them into chunks,
    create embeddings, and store every chunk
    separately in Chroma Cloud.
    """

    collection = get_collection()

    active_schemes = [
        scheme
        for scheme in schemes
        if scheme.status.lower() == "active"
    ]

    if not active_schemes:
        print("No active schemes found for indexing.")
        return

    ids = []
    documents = []
    metadatas = []

    for scheme in active_schemes:

        # Step 1: Convert scheme into a readable document
        full_document = build_document(scheme)

        # Step 2: Split the document into chunks
        chunks = chunk_document(full_document)

        # Step 3: Store every chunk separately
        for chunk_index, chunk in enumerate(chunks):

            chunk_id = f"{scheme.id}_chunk_{chunk_index}"

            ids.append(chunk_id)

            documents.append(chunk)

            metadatas.append({
                "scheme_id": scheme.id,
                "name": scheme.name,
                "category": scheme.category,
                "status": scheme.status,
                "state": scheme.state or "All",
                "chunk_index": chunk_index
            })

    if not documents:
        print("No chunks were created.")
        return

    print(
        f"Created {len(documents)} chunks "
        f"from {len(active_schemes)} schemes."
    )

    # Step 4: Create embeddings for every chunk
    embeddings = embed_texts(documents)

    # Step 5: Store chunk vectors in Chroma Cloud
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(
        f"Successfully stored {len(documents)} "
        f"chunks in Chroma Cloud."
    )


def reset_index():
    """
    Delete the existing schemes collection
    from Chroma Cloud.
    """

    global _client

    client = get_chroma_client()

    try:
        client.delete_collection(name="schemes")
        print("Old Chroma Cloud collection deleted.")

    except Exception as error:
        print(
            "No existing Chroma Cloud collection found "
            f"or deletion skipped: {error}"
        )

    _client = None