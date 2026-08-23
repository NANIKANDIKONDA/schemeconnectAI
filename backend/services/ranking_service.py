from typing import List, Dict, Any


# ==========================================================
# CATEGORY KEYWORDS
# ==========================================================

CATEGORY_KEYWORDS = {
    "Agriculture": [
        "farmer",
        "agriculture",
        "agricultural",
        "farming",
        "crop",
        "crops",
        "land",
        "cultivation",
        "rythu",
        "kisan",
    ],

    "Education": [
        "student",
        "education",
        "scholarship",
        "college",
        "school",
        "b.tech",
        "btech",
        "degree",
        "university",
        "study",
        "studies",
        "fee",
    ],

    "Healthcare": [
        "health",
        "healthcare",
        "hospital",
        "medical",
        "treatment",
        "medicine",
        "illness",
        "disease",
        "insurance",
    ],

    "Employment": [
        "job",
        "employment",
        "worker",
        "work",
        "business",
        "entrepreneur",
        "startup",
        "wage",
        "livelihood",
    ],

    "Women Welfare": [
        "woman",
        "women",
        "female",
        "pregnant",
        "pregnancy",
        "mother",
        "maternity",
        "girl",
    ],

    "Social Welfare": [
        "welfare",
        "poverty",
        "poor",
        "family",
        "financial support",
        "social",
    ],
}


# ==========================================================
# ELIGIBILITY PRIORITY
# ==========================================================

ELIGIBILITY_SCORES = {
    "LIKELY_ELIGIBLE": 40,
    "POSSIBLY_ELIGIBLE": 25,
    "MORE_INFORMATION_REQUIRED": 15,
    "NOT_ELIGIBLE": -50,
}


# ==========================================================
# MAIN RANKING FUNCTION
# ==========================================================

def rank_schemes(
    evaluated_schemes: List[Dict[str, Any]],
    citizen_profile: Dict[str, Any] | None = None,
    user_query: str = "",
) -> List[Dict[str, Any]]:
    """
    Rank schemes using:

    1. User intent and profile relevance
    2. Scheme category relevance
    3. Eligibility status
    4. Number of matched conditions
    5. Missing information penalty
    6. Failed eligibility penalty

    Each ranked item receives a final_score.
    """

    if citizen_profile is None:
        citizen_profile = {}

    # ------------------------------------------------------
    # BUILD USER CONTEXT
    # ------------------------------------------------------

    context_parts = []

    if user_query:
        context_parts.append(user_query)

    for key in [
        "occupation",
        "user_intent",
        "education",
        "beneficiary_for",
    ]:

        value = citizen_profile.get(key)

        if value:
            context_parts.append(str(value))

    user_context = " ".join(context_parts).lower()

    occupation = str(
        citizen_profile.get("occupation") or ""
    ).lower()

    user_intent = str(
        citizen_profile.get("user_intent") or ""
    ).lower()

    education = str(
        citizen_profile.get("education") or ""
    ).lower()

    # ------------------------------------------------------
    # CALCULATE CATEGORY RELEVANCE
    # ------------------------------------------------------

    def calculate_category_score(
        scheme_category: str,
    ) -> float:

        score = 0.0

        keywords = CATEGORY_KEYWORDS.get(
            scheme_category,
            [],
        )

        # Keyword matches from query/profile
        for keyword in keywords:

            if keyword in user_context:
                score += 20

        # Strong occupation-specific boosts
        if occupation:

            if (
                occupation == "farmer"
                and scheme_category == "Agriculture"
            ):
                score += 50

            elif (
                occupation == "student"
                and scheme_category == "Education"
            ):
                score += 50

        # Strong education-specific boost
        if education and scheme_category == "Education":

            if any(
                word in education
                for word in [
                    "b.tech",
                    "btech",
                    "degree",
                    "student",
                    "college",
                ]
            ):
                score += 35

        # Intent-specific boosts
        if user_intent:

            for keyword in keywords:

                if keyword in user_intent:
                    score += 30

        return score

    # ------------------------------------------------------
    # CALCULATE FINAL SCORE
    # ------------------------------------------------------

    def calculate_final_score(
        item: Dict[str, Any],
    ) -> float:

        scheme = item["scheme"]
        result = item["result"]

        final_score = 0.0

        # 1. CATEGORY / USER CONTEXT RELEVANCE
        category_score = calculate_category_score(
            scheme.category
        )

        final_score += category_score

        # 2. ELIGIBILITY SCORE
        eligibility_status = result.get(
            "eligibility_status",
            "MORE_INFORMATION_REQUIRED",
        )

        final_score += ELIGIBILITY_SCORES.get(
            eligibility_status,
            0,
        )

        # 3. MATCHED CONDITIONS
        matched_conditions = result.get(
            "match_score",
            0,
        )

        final_score += matched_conditions * 5

        # 4. MISSING INFORMATION PENALTY
        missing_information = result.get(
            "missing_information",
            [],
        )

        final_score -= len(
            missing_information
        ) * 8

        # 5. FAILED CONDITIONS PENALTY
        failed_conditions = result.get(
            "failed_conditions",
            [],
        )

        final_score -= len(
            failed_conditions
        ) * 20

        # Store scores for debugging and future frontend use
        item["category_score"] = round(
            category_score,
            2,
        )

        item["final_score"] = round(
            final_score,
            2,
        )

        return final_score

    # ------------------------------------------------------
    # SCORE ALL SCHEMES
    # ------------------------------------------------------

    for item in evaluated_schemes:

        calculate_final_score(item)

    # ------------------------------------------------------
    # SORT HIGHEST SCORE FIRST
    # ------------------------------------------------------

    ranked_schemes = sorted(
        evaluated_schemes,
        key=lambda item: item.get(
            "final_score",
            0,
        ),
        reverse=True,
    )

    return ranked_schemes