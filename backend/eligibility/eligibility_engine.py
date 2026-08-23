from backend.models.citizen import CitizenProfile
from backend.models.scheme import Scheme


class EligibilityEngine:

    @staticmethod
    def _get_failure_reason(condition: str) -> str:
        reasons = {
            "state": "You are not from the supported state.",
            "min_age": "You do not meet the minimum age requirement.",
            "max_age": "Your age exceeds the scheme's maximum age requirement.",
            "max_income": "Your annual income exceeds the maximum allowed limit.",
            "occupation": "Your occupation is not covered under this scheme.",
            "education": "Your education level does not match the requirements.",
            "category": "Your social category is not covered under this scheme.",
            "min_land_acres": "You do not meet the minimum land ownership requirement.",
            "max_land_acres": "Your land ownership exceeds the maximum allowed limit.",
            "gender": "This scheme is restricted to a different gender."
        }

        return reasons.get(
            condition,
            f"You do not meet the {condition} requirement."
        )

    @staticmethod
    def _get_success_reason(condition: str) -> str:
        reasons = {
            "state": "You are from a supported state.",
            "min_age": "You meet the age requirements.",
            "max_age": "You meet the age requirements.",
            "max_income": "Your income is within the allowed limit.",
            "occupation": "Your occupation is eligible.",
            "education": "Your education level qualifies.",
            "category": "Your social category qualifies.",
            "min_land_acres": "Your land ownership meets the criteria.",
            "max_land_acres": "Your land ownership meets the criteria.",
            "gender": "Your gender matches the scheme criteria."
        }

        return reasons.get(
            condition,
            f"Your {condition} matches the scheme requirements."
        )

    @staticmethod
    def _determine_relevance(
        citizen: CitizenProfile,
        scheme: Scheme
    ) -> str:
        """
        Determine scheme relevance using:

        1. User intent
        2. Citizen occupation
        3. Scheme category
        4. Target beneficiaries
        """

        intent = (citizen.user_intent or "").lower()
        occupation = (citizen.occupation or "").lower()
        category = (scheme.category or "").lower()

        relevance_score = 0

        # --------------------------------------------------
        # DIRECT CATEGORY / INTENT MATCH
        # --------------------------------------------------

        if intent:

            if category in intent or intent in category:
                relevance_score += 3

            intent_category_mapping = {
                "farmer": "agriculture",
                "farming": "agriculture",
                "agriculture": "agriculture",

                "student": "education",
                "scholarship": "education",
                "education": "education",

                "health": "healthcare",
                "medical": "healthcare",
                "hospital": "healthcare",
                "healthcare": "healthcare",

                "job": "employment",
                "employment": "employment",
                "business": "employment",

                "women": "women welfare",
                "pregnancy": "women welfare",
                "maternity": "women welfare",

                "bank": "social welfare",
                "financial": "social welfare"
            }

            for keyword, mapped_category in intent_category_mapping.items():
                if keyword in intent and mapped_category == category:
                    relevance_score += 3
                    break

        # --------------------------------------------------
        # OCCUPATION → CATEGORY MATCH
        # --------------------------------------------------

        occupation_category_mapping = {
            "farmer": "agriculture",
            "student": "education",
            "worker": "employment",
            "job seeker": "employment",
            "entrepreneur": "employment",
            "businessman": "employment",
            "businesswoman": "employment"
        }

        mapped_category = occupation_category_mapping.get(occupation)

        if mapped_category == category:
            relevance_score += 3

        # --------------------------------------------------
        # SCHEME OCCUPATION MATCH
        # --------------------------------------------------

        scheme_occupations = [
            item.lower()
            for item in (scheme.eligibility.occupations or [])
        ]

        if occupation and occupation in scheme_occupations:
            relevance_score += 3

        # --------------------------------------------------
        # TARGET BENEFICIARY MATCH
        # --------------------------------------------------

        if scheme.target_beneficiaries:

            targets = [
                target.lower()
                for target in scheme.target_beneficiaries
            ]

            if occupation and occupation in targets:
                relevance_score += 2

            if citizen.beneficiary_for:

                beneficiary = citizen.beneficiary_for.lower()

                beneficiary_mapping = {
                    "daughter": "girl_child",
                    "son": "child",
                    "wife": "women",
                    "mother": "women"
                }

                mapped_beneficiary = beneficiary_mapping.get(
                    beneficiary,
                    beneficiary
                )

                if mapped_beneficiary in targets:
                    relevance_score += 3

        # --------------------------------------------------
        # FINAL RELEVANCE
        # --------------------------------------------------

        if relevance_score >= 5:
            return "HIGHLY_RELEVANT"

        if relevance_score >= 3:
            return "RELEVANT"

        if relevance_score >= 1:
            return "POSSIBLY_RELEVANT"

        return "LOW_RELEVANCE"

    @staticmethod
    def check_eligibility(
        citizen: CitizenProfile,
        scheme: Scheme
    ) -> dict:

        matched = []
        failed = []
        missing = []

        elig = scheme.eligibility

        # --------------------------------------------------
        # STATE CHECK
        # --------------------------------------------------

        allowed_states = list(elig.states or [])

        if scheme.state and scheme.state != "All":

            if scheme.state not in allowed_states:
                allowed_states.append(scheme.state)

        if allowed_states and "All" not in allowed_states:

            if not citizen.state:
                missing.append("state")

            elif citizen.state not in allowed_states:
                failed.append("state")

            else:
                matched.append("state")

        # --------------------------------------------------
        # AGE CHECKS
        # --------------------------------------------------

        if elig.min_age is not None:

            if citizen.age is None:
                missing.append("age")

            elif citizen.age < elig.min_age:
                failed.append("min_age")

            else:
                matched.append("min_age")

        if elig.max_age is not None:

            if citizen.age is None:
                missing.append("age")

            elif citizen.age > elig.max_age:
                failed.append("max_age")

            else:

                if (
                    "min_age" not in matched
                    and "max_age" not in matched
                ):
                    matched.append("max_age")

        # --------------------------------------------------
        # INCOME CHECK
        # --------------------------------------------------

        if elig.max_income is not None:

            if citizen.annual_income is None:
                missing.append("annual_income")

            elif citizen.annual_income > elig.max_income:
                failed.append("max_income")

            else:
                matched.append("max_income")

        # --------------------------------------------------
        # OCCUPATION CHECK
        # --------------------------------------------------

        if elig.occupations:

            if not citizen.occupation:
                missing.append("occupation")

            else:

                citizen_occupation = citizen.occupation.lower()

                allowed_occupations = [
                    occupation.lower()
                    for occupation in elig.occupations
                ]

                if citizen_occupation not in allowed_occupations:
                    failed.append("occupation")

                else:
                    matched.append("occupation")

        # --------------------------------------------------
        # EDUCATION CHECK
        # --------------------------------------------------

        if elig.education:

            if not citizen.education:
                missing.append("education")

            else:

                citizen_education = citizen.education.lower()

                allowed_education = [
                    education.lower()
                    for education in elig.education
                ]

                if citizen_education not in allowed_education:
                    failed.append("education")

                else:
                    matched.append("education")

        # --------------------------------------------------
        # CATEGORY CHECK
        # --------------------------------------------------

        if elig.categories:

            if not citizen.category:
                missing.append("category")

            else:

                citizen_category = citizen.category.lower()

                allowed_categories = [
                    category.lower()
                    for category in elig.categories
                ]

                if citizen_category not in allowed_categories:
                    failed.append("category")

                else:
                    matched.append("category")

        # --------------------------------------------------
        # LAND CHECKS
        # --------------------------------------------------

        if elig.min_land_acres is not None:

            if citizen.land_acres is None:
                missing.append("land_acres")

            elif citizen.land_acres < elig.min_land_acres:
                failed.append("min_land_acres")

            else:
                matched.append("min_land_acres")

        if elig.max_land_acres is not None:

            if citizen.land_acres is None:
                missing.append("land_acres")

            elif citizen.land_acres > elig.max_land_acres:
                failed.append("max_land_acres")

            else:

                if (
                    "min_land_acres" not in matched
                    and "max_land_acres" not in matched
                ):
                    matched.append("max_land_acres")

        # --------------------------------------------------
        # GENDER CHECK
        # --------------------------------------------------

        if elig.genders:

            if not citizen.gender:
                missing.append("gender")

            else:

                citizen_gender = citizen.gender.lower()

                allowed_genders = [
                    gender.lower()
                    for gender in elig.genders
                ]

                if citizen_gender not in allowed_genders:
                    failed.append("gender")

                else:
                    matched.append("gender")

        # --------------------------------------------------
        # REMOVE DUPLICATES
        # --------------------------------------------------

        missing = list(dict.fromkeys(missing))
        matched = list(dict.fromkeys(matched))
        failed = list(dict.fromkeys(failed))

        # --------------------------------------------------
        # EXPLANATIONS
        # --------------------------------------------------

        failed_explanations = [
            EligibilityEngine._get_failure_reason(condition)
            for condition in failed
        ]

        success_explanations = list(
            dict.fromkeys(
                EligibilityEngine._get_success_reason(condition)
                for condition in matched
            )
        )

        if not success_explanations and not failed:

            success_explanations = [
                "Your profile broadly matches the scheme's general criteria."
            ]

        # --------------------------------------------------
        # ELIGIBILITY STATUS
        # --------------------------------------------------

        if failed:

            status = "NOT_ELIGIBLE"

        elif missing:

            if matched:
                status = "POSSIBLY_ELIGIBLE"

            else:
                status = "MORE_INFORMATION_REQUIRED"

        else:

            status = "LIKELY_ELIGIBLE"

        # --------------------------------------------------
        # RELEVANCE STATUS
        # --------------------------------------------------

        relevance = EligibilityEngine._determine_relevance(
            citizen,
            scheme
        )

        # --------------------------------------------------
        # RETURN RESULT
        # --------------------------------------------------

        return {
            "eligibility_status": status,
            "relevance_status": relevance,
            "matched_conditions": matched,
            "failed_conditions": failed_explanations,
            "missing_information": missing,
            "match_score": len(matched),
            "success_reasons": success_explanations
        }