import json
from typing import Dict, List, Any

from backend.llm.gemini_client import generate_text


def generate_rag_response(
    user_message: str,
    profile: Dict[str, Any],
    context: str,
    ranked_schemes: List[Dict[str, Any]],
) -> str:
    """
    Generate a final answer using Gemini.

    The answer is grounded in:
    1. User's question
    2. Citizen profile
    3. Chunks retrieved from ChromaDB
    4. Verified eligibility and ranking results
    """

    if not ranked_schemes:
        return (
            "I could not find any relevant government schemes "
            "based on your current information."
        )

    # --------------------------------------------
    # Prepare verified backend results
    # --------------------------------------------

    verified_results = []

    for item in ranked_schemes[:5]:
        scheme = item.get("scheme")
        result = item.get("result", {})

        if scheme is None:
            continue

        verified_results.append(
            {
                "scheme_name": scheme.name,
                "category": scheme.category,
                "eligibility_status": result.get(
                    "eligibility_status"
                ),
                "matched_conditions": result.get(
                    "matched_conditions",
                    result.get("match_score", 0),
                ),
                "missing_information": result.get(
                    "missing_information",
                    [],
                ),
                "failed_conditions": result.get(
                    "failed_conditions",
                    [],
                ),
                "official_source": scheme.official_link,
            }
        )

    # --------------------------------------------
    # Safety fallback
    # --------------------------------------------

    if not verified_results:
        return (
            "I found some scheme information, but I could not "
            "generate a verified eligibility response."
        )

    profile_json = json.dumps(
        profile,
        indent=2,
        default=str,
    )

    verified_json = json.dumps(
        verified_results,
        indent=2,
        default=str,
    )

    # --------------------------------------------
    # RAG Prompt
    # --------------------------------------------

    prompt = f"""
You are SchemeConnect AI, an assistant that helps Indian citizens
understand government schemes.

Your task is to answer the user's question using ONLY the retrieved
scheme information and verified backend eligibility results provided below.

IMPORTANT RULES:

1. Use ONLY the information in the retrieved context.
2. Do NOT invent scheme names, benefits, eligibility criteria,
   documents, application steps, or official websites.
3. Do NOT change the eligibility status calculated by the backend.
4. Clearly mention if a scheme is:
   - LIKELY_ELIGIBLE
   - POSSIBLY_ELIGIBLE
   - MORE_INFORMATION_REQUIRED
   - NOT_ELIGIBLE
5. If retrieved information does not answer the question, clearly say so.
6. Keep the answer helpful, concise, and easy for an ordinary citizen
   to understand.
7. Do not mention ChromaDB, embeddings, chunks, vectors, RAG,
   retrieval pipeline, or internal backend systems.
8. Never claim that the user is definitely approved for a scheme.
   Explain that final eligibility must be verified through official sources.

USER QUESTION:
{user_message}

CITIZEN PROFILE:
{profile_json}

VERIFIED ELIGIBILITY RESULTS:
{verified_json}

RETRIEVED SCHEME CONTEXT:
{context}

Generate a clear and helpful response for the user.
"""

    # --------------------------------------------
    # Gemini Generation
    # --------------------------------------------

    try:
        response = generate_text(prompt)

        if response and response.strip():
            return response.strip()

    except Exception as e:
        print(f"RAG generation error: {e}")

    # --------------------------------------------
    # Fallback Response
    # --------------------------------------------

    fallback_lines = [
        "Based on your information, here are the most relevant schemes:"
    ]

    for item in verified_results[:3]:
        fallback_lines.append(
            f"\n{item['scheme_name']}"
        )

        fallback_lines.append(
            f"Status: {item['eligibility_status']}"
        )

        fallback_lines.append(
            f"Official Source: {item['official_source']}"
        )

    fallback_lines.append(
        "\nPlease verify the final eligibility and application "
        "requirements through the official government source."
    )

    return "\n".join(fallback_lines)