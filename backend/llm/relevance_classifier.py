import re

from backend.llm.gemini_client import generate_structured_json


# ==========================================================
# DOMAIN KEYWORDS
# ==========================================================

DOMAIN_KEYWORDS = [
    "scheme",
    "schemes",
    "government scheme",
    "government schemes",
    "welfare",
    "benefit",
    "benefits",
    "eligible",
    "eligibility",
    "qualify",
    "subsidy",
    "subsidies",
    "financial assistance",
    "scholarship",
    "pension",
    "farmer",
    "agriculture",
    "crop",
    "student",
    "education",
    "employment",
    "unemployment",
    "housing",
    "healthcare",
    "medical scheme",
    "ration",
    "loan",
    "startup",
    "documents required",
    "how to apply",
    "application",
    "apply for",
]


# ==========================================================
# CHECK PROFILE / FOLLOW-UP INFORMATION
# ==========================================================

def looks_like_profile_information(message: str) -> bool:
    """
    Detect messages that provide useful citizen profile
    information during a conversation.
    """

    text = message.lower().strip()

    # Pure numeric answer such as:
    # 20
    # 150000
    if re.fullmatch(r"\d+(?:\.\d+)?", text):
        return True

    patterns = [
        r"\b\d{1,3}\s+years?\s+old\b",
        r"\bage\s*(?:is|:)?\s*\d+\b",
        r"\bi am\s+\d{1,3}\b",
        r"\bannual income\b",
        r"\bmy income\b",
        r"\bincome is\b",
        r"\bearn\b",
        r"\b\d+(?:\.\d+)?\s*acres?\b",
        r"\bfarmer\b",
        r"\bstudent\b",
        r"\bunemployed\b",
        r"\bemployee\b",
        r"\bmale\b",
        r"\bfemale\b",
        r"\bwoman\b",
        r"\bgirl\b",
        r"\bman\b",
        r"\bboy\b",
        r"\bsc\b",
        r"\bst\b",
        r"\bobc\b",
        r"\bews\b",
        r"\bandhra pradesh\b",
        r"\btelangana\b",
        r"\btamil nadu\b",
        r"\bkarnataka\b",
        r"\bkerala\b",
        r"\bmaharashtra\b",
        r"\bdelhi\b",
        r"\bbihar\b",
        r"\bodisha\b",
        r"\bpunjab\b",
        r"\bgujarat\b",
    ]

    return any(
        re.search(pattern, text)
        for pattern in patterns
    )


# ==========================================================
# FAST LOCAL CHECK
# ==========================================================

def is_obviously_scheme_related(message: str) -> bool:
    """
    Fast local check for clearly relevant questions.
    """

    text = message.lower()

    return any(
        keyword in text
        for keyword in DOMAIN_KEYWORDS
    )


# ==========================================================
# GEMINI RELEVANCE CLASSIFIER
# ==========================================================

def classify_relevance(message: str) -> bool:
    """
    Use Gemini only when the message is not clearly
    identifiable using local rules.

    Returns:
        True  -> relevant to SchemeConnect AI
        False -> irrelevant
    """

    prompt = f"""
You are a strict domain classifier for SchemeConnect AI.

SchemeConnect AI ONLY helps Indian citizens with:

- Government welfare schemes
- Government benefits
- Eligibility checking
- Scholarships
- Agriculture and farmer support
- Healthcare schemes
- Employment or self-employment schemes
- Housing schemes
- Subsidies
- Pensions
- Government financial assistance
- Documents and application procedures for schemes

Determine whether the following user message is relevant
to this domain.

A message can also be relevant if it provides personal
information needed to check eligibility, such as age,
state, occupation, income, education, category, gender,
or land ownership.

Return ONLY this JSON:

{{
    "relevant": true
}}

or

{{
    "relevant": false
}}

Do not answer the user's question.
Only classify relevance.

User message:
"{message}"
"""

    try:

        result = generate_structured_json(prompt)

        if isinstance(result, dict):

            return bool(
                result.get("relevant", False)
            )

    except Exception as error:

        print(
            f"Relevance classification error: {error}"
        )

    # Safe fallback:
    # If Gemini is unavailable, only allow messages
    # that are clearly related locally.
    return is_obviously_scheme_related(message)


# ==========================================================
# MAIN RELEVANCE FUNCTION
# ==========================================================

def is_scheme_related(message: str) -> bool:
    """
    Main relevance detection function.
    """

    # 1. Profile information
    if looks_like_profile_information(message):
        return True

    # 2. Clearly scheme-related
    if is_obviously_scheme_related(message):
        return True

    # 3. Ambiguous natural-language question
    return classify_relevance(message)