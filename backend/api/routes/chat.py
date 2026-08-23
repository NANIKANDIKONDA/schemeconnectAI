import json
import os
import uuid

from typing import Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.models.scheme import Scheme
from backend.conversation.conversation_manager import ConversationManager

from backend.conversation.chat_history_store import (
    save_chat_message,
    get_chat_history,
    delete_chat_history
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

conversation_sessions: Dict[str, ConversationManager] = {}


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
    Get the existing conversation for a session.
    Create a new conversation if necessary.
    """

    if session_id not in conversation_sessions:

        schemes = get_all_schemes()

        conversation_sessions[session_id] = (
            ConversationManager(schemes)
        )

    return conversation_sessions[session_id]


# ==========================================================
# RELEVANCE CHECK
# ==========================================================

def is_scheme_related(message: str, session_id: str | None = None) -> bool:
    """
    Check whether the user's message is related to government
    schemes, eligibility, benefits, applications, or is a valid
    follow-up answer in an existing conversation.
    """

    message = message.lower().strip()

    # Direct scheme-related words
    scheme_keywords = [

        # General
        "scheme",
        "schemes",
        "government scheme",
        "government schemes",
        "welfare",
        "welfare scheme",
        "eligible",
        "eligibility",
        "qualify",
        "qualification",

        # Benefits
        "benefit",
        "benefits",
        "financial assistance",
        "support",
        "subsidy",
        "subsidies",

        # Application
        "apply",
        "application",
        "apply for",
        "how to apply",
        "documents",
        "document",
        "required documents",
        "registration",
        "deadline",

        # Agriculture
        "farmer",
        "farming",
        "agriculture",
        "agricultural",
        "crop",
        "land",
        "acre",
        "acres",

        # Education
        "student",
        "students",
        "education",
        "scholarship",
        "college",
        "school",

        # Employment
        "employment",
        "job",
        "jobs",
        "unemployment",
        "self employment",
        "startup",
        "business",
        "loan",

        # Social welfare
        "pension",
        "housing",
        "health",
        "healthcare",
        "medical",
        "ration",
        "women",
        "woman",
        "girl",
        "senior citizen",
        "disabled",
        "disability",

        # Common government schemes
        "pm-kisan",
        "pm kisan",
        "rythu bharosa",
        "ysr rythu bharosa",
        "sukanya",
        "ayushman",
        "aadhar",
        "aadhaar",
    ]

    # Profile information.
    # These are important because users may answer follow-up
    # questions with only age, income, location, etc.
    profile_keywords = [

        "years old",
        "year old",
        "i am",
        "my age",
        "age is",

        "income",
        "annual income",
        "salary",
        "earn",
        "earning",

        "rupees",
        "rupee",
        "rs",
        "₹",
        "lakh",
        "lakhs",

        "andhra pradesh",
        "telangana",
        "india",

        "male",
        "female",

        "farmer",
        "student",
        "worker",
        "employee",
        "unemployed",

        "acre",
        "acres",
        "land"
    ]

    all_keywords = scheme_keywords + profile_keywords

    # Check keywords
    if any(keyword in message for keyword in all_keywords):
        return True

    # ------------------------------------------------------
    # Allow short answers during an existing conversation.
    #
    # Example:
    # Bot: "Please provide your age."
    # User: "20"
    #
    # This should NOT be considered irrelevant.
    # ------------------------------------------------------

    if session_id and session_id in conversation_sessions:

        # Allow numeric or short follow-up answers
        words = message.split()

        if len(words) <= 10:
            return True

    return False


# ==========================================================
# CHAT ENDPOINT
# ==========================================================

@router.post("/chat")
def chat(request: ChatRequest):

    try:

        user_message = request.message.strip()

        # ----------------------------------------------
        # EMPTY MESSAGE CHECK
        # ----------------------------------------------

        if not user_message:
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty."
            )

        # ----------------------------------------------
        # GENERATE SESSION ID IF NEEDED
        # ----------------------------------------------

        session_id = request.session_id

        if not session_id:
            session_id = str(uuid.uuid4())

        # ----------------------------------------------
        # RELEVANCE CHECK
        # ----------------------------------------------

        if not is_scheme_related(
            user_message,
            session_id
        ):

            result = {
                "response_type": "irrelevant",
                "message": (
                    "I'm sorry, but I am not able to answer this question. "
                    "I can only help you find government schemes, understand "
                    "scheme benefits, check your eligibility, and guide you "
                    "through the application process."
                ),
                "profile": {},
                "missing_information": [],
                "schemes": [],
                "session_id": session_id
            }

            # Save irrelevant conversation messages
            save_chat_message(
                session_id=session_id,
                role="user",
                content=user_message
            )

            save_chat_message(
                session_id=session_id,
                role="assistant",
                content=result["message"]
            )

            return result

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
        # PROCESS MESSAGE THROUGH RAG PIPELINE
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
                content=result["message"]
            )

        # ----------------------------------------------
        # ADD SESSION ID
        # ----------------------------------------------

        result["session_id"] = session_id

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
def clear_chat(session_id: str):

    try:

        # Remove conversation from RAM
        if session_id in conversation_sessions:

            del conversation_sessions[session_id]

        # Remove chat history from Chroma Cloud
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