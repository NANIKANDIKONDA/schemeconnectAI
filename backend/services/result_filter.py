from typing import List, Dict


def filter_final_results(
    ranked_schemes: List[Dict],
    include_not_eligible: bool = False
) -> List[Dict]:
    """
    Filters schemes before sending final recommendations.

    Main recommendations should prioritize schemes that are:
    - LIKELY_ELIGIBLE
    - POSSIBLY_ELIGIBLE
    - MORE_INFORMATION_REQUIRED

    NOT_ELIGIBLE schemes are removed by default.
    """

    if include_not_eligible:
        return ranked_schemes

    filtered = []

    for item in ranked_schemes:
        result = item.get("result", {})

        eligibility_status = result.get("eligibility_status")

        if eligibility_status != "NOT_ELIGIBLE":
            filtered.append(item)

    return filtered