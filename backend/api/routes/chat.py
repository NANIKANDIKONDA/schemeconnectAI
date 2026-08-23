import json
import os
import uuid

from typing import Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.models.scheme import Scheme

from backend.conversation.conversation_manager import (
    ConversationManager
)

from backend.conversation.chat_history_store import (
    save_chat_message,
    get_chat_history,
    delete_chat_history
)

from backend.llm.relevance_classifier import (
    is_scheme_related
)


# ==========================================================
# FASTAPI ROUTER
# ==========================================================

router = APIRouter()


# ==========================================================
# REQUEST MODEL
# ==========================================================

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


# ==========================================================
# SESSION STORAGE
# ==========================================================

conversation_sessions: Dict[
    str,
    ConversationManager
] = {}


# ==========================================================
# SCHEME CACHE
# ==========================================================

_schemes_cache = None


# ==========================================================
# LOAD ALL SCHEMES
# ==========================================================

def get_all_schemes() -> List[Scheme]:
    """
    Load schemes.json once and cache the Scheme objects.
    """

    global _schemes_cache

    if _schemes_cache is not None:
        return _schemes_cache

    base_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "data"
        )
    )

    schemes_path = os.path.join(
        base_dir,
        "schemes.json"
    )

    if not os.path.exists(schemes_path):

        raise FileNotFoundError(
            f"schemes.json not found at: {schemes_path}"
        )

    with open(
        schemes_path,
        "r",
        encoding="utf-8"
    ) as file:

        schemes_data = json.load(file)

    _schemes_cache = [
        Scheme(**scheme)
        for scheme in schemes_data
    ]

    return _schemes_cache


# ==========================================================
# GET OR CREATE CONVERSATION MANAGER
# ==========================================================

def get_conversation_manager(
    session_id: str
) -> ConversationManager:
    """
    Get the existing conversation manager.

    Create a new conversation if necessary.
    """

    if session_id not in conversation_sessions:

        schemes = get_all_schemes()

        conversation_sessions[
            session_id
        ] = ConversationManager(
            schemes
        )

    return conversation_sessions[
        session_id
    ]


# ==========================================================
# CHAT ENDPOINT
# ==========================================================

@router.post("/chat")
def chat(request: ChatRequest):

    try:

        # ----------------------------------------------
        # CLEAN USER MESSAGE
        # ----------------------------------------------

        user_message = request.message.strip()

        if not user_message:

            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty."
            )

        # ----------------------------------------------
        # GENERATE SESSION ID
        # ----------------------------------------------

        session_id = request.session_id

        if not session_id:

            session_id = str(
                uuid.uuid4()
            )

        # ----------------------------------------------
        # CHECK QUESTION RELEVANCE
        # ----------------------------------------------

        if not is_scheme_related(
            user_message
        ):

            response_message = (
                "I'm sorry, but I am not able to answer "
                "this question. I can only help you find "
                "government schemes, understand scheme "
                "benefits, check your eligibility, and "
                "guide you through the application process."
            )

            # Save user message
            save_chat_message(
                session_id=session_id,
                role="user",
                content=user_message
            )

            # Save assistant response
            save_chat_message(
                session_id=session_id,
                role="assistant",
                content=response_message
            )

            return {
                "response_type": "irrelevant",

                "message": response_message,

                "profile": {},

                "missing_information": [],

                "schemes": [],

                "session_id": session_id
            }

        # ----------------------------------------------
        # SAVE USER MESSAGE
        # ----------------------------------------------

        save_chat_message(
            session_id=session_id,
            role="user",
            content=user_message
        )

        # ----------------------------------------------
        # GET CONVERSATION MANAGER
        # ----------------------------------------------

        manager = get_conversation_manager(
            session_id
        )

        # ----------------------------------------------
        # PROCESS MESSAGE
        #
        # Existing pipeline:
        #
        # Profile Extraction
        #        ↓
        # Missing Information
        #        ↓
        # Scheme Filtering
        #        ↓
        # RAG Retrieval
        #        ↓
        # Eligibility Engine
        #        ↓
        # Ranking
        #        ↓
        # Gemini Response
        # ----------------------------------------------

        result = manager.process_message(
            user_message
        )

        # ----------------------------------------------
        # SAVE AI RESPONSE
        # ----------------------------------------------

        if result.get("message"):

            save_chat_message(
                session_id=session_id,
                role="assistant",
                content=result[
                    "message"
                ]
            )

        # ----------------------------------------------
        # ADD SESSION ID
        # ----------------------------------------------

        result[
            "session_id"
        ] = session_id

        return result

    except HTTPException:

        raise

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    except Exception as error:

        print(
            f"Chat API Error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ==========================================================
# GET CHAT HISTORY
# ==========================================================

@router.get("/chat/{session_id}/history")
def fetch_chat_history(
    session_id: str
):

    try:

        history = get_chat_history(
            session_id
        )

        return {
            "session_id": session_id,
            "messages": history
        }

    except Exception as error:

        print(
            f"Get history error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ==========================================================
# DELETE / CLEAR SESSION
# ==========================================================

@router.delete("/chat/{session_id}")
def clear_chat(
    session_id: str
):

    try:

        # ----------------------------------------------
        # REMOVE CONVERSATION FROM MEMORY
        # ----------------------------------------------

        if session_id in conversation_sessions:

            del conversation_sessions[
                session_id
            ]

        # ----------------------------------------------
        # DELETE CHAT HISTORY
        # ----------------------------------------------

        delete_chat_history(
            session_id
        )

        return {
            "message": (
                "Conversation cleared successfully."
            ),

            "session_id": session_id
        }

    except Exception as error:

        print(
            f"Clear chat error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )