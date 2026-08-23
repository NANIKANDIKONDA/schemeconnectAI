from datetime import datetime, timezone
from typing import List, Dict
import uuid

from backend.rag.vector_store import get_chroma_client


COLLECTION_NAME = "chat_history"


def get_chat_history_collection():
    """
    Get or create the Chroma Cloud collection
    used for storing chat messages.
    """

    client = get_chroma_client()

    return client.get_or_create_collection(
        name=COLLECTION_NAME
    )


def save_chat_message(
    session_id: str,
    role: str,
    content: str
):
    """
    Save one chat message to Chroma Cloud.
    """

    collection = get_chat_history_collection()

    message_id = str(uuid.uuid4())

    timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    collection.add(
        ids=[message_id],

        documents=[
            content
        ],

        metadatas=[
            {
                "session_id": session_id,
                "role": role,
                "timestamp": timestamp
            }
        ]
    )

    return message_id


def get_chat_history(
    session_id: str,
    limit: int = 50
) -> List[Dict]:
    """
    Get all chat messages belonging to one session.
    """

    collection = get_chat_history_collection()

    results = collection.get(
        where={
            "session_id": session_id
        },
        include=[
            "documents",
            "metadatas"
        ]
    )

    messages = []

    ids = results.get("ids", [])
    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

    for message_id, document, metadata in zip(
        ids,
        documents,
        metadatas
    ):

        messages.append(
            {
                "id": message_id,
                "role": metadata.get("role"),
                "content": document,
                "timestamp": metadata.get(
                    "timestamp"
                )
            }
        )

    # Sort messages by timestamp
    messages.sort(
        key=lambda x: x.get(
            "timestamp",
            ""
        )
    )

    return messages[-limit:]


def delete_chat_history(
    session_id: str
):
    """
    Delete all chat messages for one session.
    """

    collection = get_chat_history_collection()

    collection.delete(
        where={
            "session_id": session_id
        }
    )