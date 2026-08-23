def determine_missing_important_info(profile: dict) -> list[str]:
    """
    Return useful missing information based on the user's profile and intent.

    IMPORTANT:
    These fields do NOT block scheme discovery.
    They are used to:
    1. Inform the user what additional details could improve accuracy.
    2. Allow the eligibility engine to mark individual schemes as
       POSSIBLY_ELIGIBLE or MORE_INFORMATION_REQUIRED.
    """

    intent = (profile.get("user_intent") or "").lower()
    occupation = (profile.get("occupation") or "").lower()

    missing = []

    # --------------------------------------------------
    # Basic information
    # --------------------------------------------------

    if not profile.get("state"):
        missing.append("state")

    # --------------------------------------------------
    # Agriculture / Farmer
    # --------------------------------------------------

    is_farmer = (
        "agriculture" in intent
        or "farming" in intent
        or occupation == "farmer"
    )

    if is_farmer:

        if not profile.get("age"):
            missing.append("age")

        if profile.get("land_acres") is None:
            missing.append("land_acres")

        if profile.get("annual_income") is None:
            missing.append("annual_income")

    # --------------------------------------------------
    # Student / Education / Scholarship
    # --------------------------------------------------

    is_student = (
        "scholarship" in intent
        or "education" in intent
        or occupation == "student"
    )

    if is_student:

        if not profile.get("age"):
            missing.append("age")

        # Education level may be needed for some schemes
        if not profile.get("education"):
            missing.append("education")

        # Income may be needed for some schemes
        if profile.get("annual_income") is None:
            missing.append("annual_income")

        # Category is scheme-specific, so keep it as useful info
        if not profile.get("category"):
            missing.append("category")

    # --------------------------------------------------
    # General scheme search
    # --------------------------------------------------

    if not is_farmer and not is_student:

        if not profile.get("age"):
            missing.append("age")

        if profile.get("annual_income") is None:
            missing.append("annual_income")

    # Remove duplicates while preserving order
    unique_missing = []

    for field in missing:
        if field not in unique_missing:
            unique_missing.append(field)

    return unique_missing