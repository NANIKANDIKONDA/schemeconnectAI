from typing import Any


def build_rag_query(
    user_message: str,
    profile: dict[str, Any]
) -> str:
    """
    Build a profile-aware query for semantic scheme retrieval.

    Only profile fields that contain actual values are included.
    """

    lines = [
        "Government scheme search request:",
        user_message.strip(),
        "",
        "Citizen profile:"
    ]

    field_labels = {
        "age": "Age",
        "state": "State",
        "occupation": "Occupation",
        "annual_income": "Annual income",
        "education": "Education",
        "category": "Social category",
        "land_acres": "Land owned in acres",
        "gender": "Gender",
        "beneficiary_for": "Beneficiary for",
        "user_intent": "User intent",
    }

    has_profile_data = False

    for field, label in field_labels.items():
        value = profile.get(field)

        if value is not None and value != "":
            lines.append(f"{label}: {value}")
            has_profile_data = True

    if not has_profile_data:
        lines.append("No additional profile information available.")

    lines.extend([
        "",
        "Task:",
        (
            "Find the government schemes that are most relevant "
            "to the citizen's request, profile, state, occupation, "
            "education, income, land ownership, and beneficiary needs."
        ),
    ])

    return "\n".join(lines)