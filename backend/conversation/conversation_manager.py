from backend.llm.profile_extractor import extract_profile_from_message
from backend.conversation.missing_info import determine_missing_important_info

from backend.models.citizen import CitizenProfile

from backend.services.scheme_filter import filter_schemes

from backend.rag.retriever import retrieve_relevant_schemes
from backend.rag.context_builder import build_rag_context

from backend.eligibility.eligibility_engine import EligibilityEngine
from backend.services.ranking_service import rank_schemes

from backend.llm.response_generator import generate_clarification_request

from backend.services.generation_service import generate_rag_response


class ConversationManager:

    def __init__(self, all_schemes):
        """
        Store all schemes and maintain the user's
        conversation profile.
        """

        self.session_profile = {}
        self.all_schemes = all_schemes


    def process_message(self, user_message: str) -> dict:
        """
        Complete SchemeConnect AI pipeline.

        Flow:

        User Message
             ↓
        Profile Extraction
             ↓
        Missing Information Check
             ↓
        Scheme Filtering
             ↓
        ChromaDB Retrieval
             ↓
        Build RAG Context
             ↓
        Eligibility Engine
             ↓
        Ranking
             ↓
        Gemini Generation
             ↓
        Final Response
        """

        # ==================================================
        # STEP 1 — Extract information from user message
        # ==================================================

        self.session_profile = extract_profile_from_message(
            user_message,
            self.session_profile
        )


        # ==================================================
        # STEP 2 — Check missing information
        # ==================================================

        missing_fields = determine_missing_important_info(
            self.session_profile
        )


        # Ask only once for missing information
        if (
            missing_fields
            and not self.session_profile.get("_has_asked_missing")
        ):

            self.session_profile["_has_asked_missing"] = True

            clarification = generate_clarification_request(
                missing_fields,
                self.session_profile.get("user_intent")
            )

            return {
                "response_type": "follow_up",
                "message": clarification,
                "profile": self._clean_profile(),
                "missing_information": missing_fields,
                "schemes": []
            }


        # ==================================================
        # STEP 3 — Create CitizenProfile
        # ==================================================

        citizen_kwargs = {
            key: value
            for key, value in self.session_profile.items()
            if not key.startswith("_")
        }

        citizen = CitizenProfile(
            **citizen_kwargs
        )


        # ==================================================
        # STEP 4 — Smart scheme filtering
        # ==================================================

        filtered_schemes = filter_schemes(
            self.all_schemes,
            citizen
        )


        if not filtered_schemes:

            return {
                "response_type": "no_results",
                "message": (
                    "I could not find any schemes matching "
                    "your current profile."
                ),
                "profile": self._clean_profile(),
                "missing_information": [],
                "schemes": []
            }


        # ==================================================
        # STEP 5 — Build semantic search query
        # ==================================================

        intent = citizen.user_intent or "government schemes"

        query = f"""
User request: {user_message}

User intent: {intent}

Occupation: {citizen.occupation}

State: {citizen.state}

Find the most relevant government schemes and information
related to the user's request.
"""


        # ==================================================
        # STEP 6 — Retrieve relevant chunks from ChromaDB
        # ==================================================

        retrieved_results = retrieve_relevant_schemes(
            query,
            filtered_schemes,
            top_k=5
        )


        if not retrieved_results:

            return {
                "response_type": "no_results",
                "message": (
                    "I could not find relevant scheme information "
                    "for your request."
                ),
                "profile": self._clean_profile(),
                "missing_information": [],
                "schemes": []
            }


        # ==================================================
        # STEP 7 — Build RAG context
        # ==================================================

        rag_context = build_rag_context(
            retrieved_results
        )


        # ==================================================
        # STEP 8 — Get retrieved scheme IDs
        # ==================================================

        retrieved_ids = [
            result["id"]
            for result in retrieved_results
        ]


        # ==================================================
        # STEP 9 — Get full scheme objects
        # ==================================================

        retrieved_schemes = [
            scheme
            for scheme in filtered_schemes
            if scheme.id in retrieved_ids
        ]


        # ==================================================
        # STEP 10 — Eligibility evaluation
        # ==================================================

        evaluated_schemes = []

        for scheme in retrieved_schemes:

            eligibility_result = (
                EligibilityEngine.check_eligibility(
                    citizen,
                    scheme
                )
            )

            evaluated_schemes.append(
                {
                    "scheme": scheme,
                    "result": eligibility_result
                }
            )


        # ==================================================
        # STEP 11 — Rank schemes
        # ==================================================

        ranked_schemes = rank_schemes(
            evaluated_schemes
        )


        # ==================================================
        # STEP 12 — Generate final RAG response using Gemini
        # ==================================================

        final_message = generate_rag_response(
            user_message=user_message,
            profile=citizen.model_dump(),
            context=rag_context,
            ranked_schemes=ranked_schemes
        )


        # ==================================================
        # STEP 13 — Prepare structured scheme results
        # ==================================================

        scheme_results = []

        for item in ranked_schemes[:5]:

            scheme = item["scheme"]

            result = item["result"]

            scheme_results.append(
                {
                    "id": scheme.id,
                    "name": scheme.name,
                    "category": scheme.category,

                    "eligibility_status":
                        result.get("eligibility_status"),

                    "relevance":
                        result.get("relevance_status"),

                    "matched_conditions":
                        result.get("match_score", 0),

                    "missing_information":
                        result.get(
                            "missing_information",
                            []
                        ),

                    "failed_conditions":
                        result.get(
                            "failed_conditions",
                            []
                        ),

                    "success_reasons":
                        result.get(
                            "success_reasons",
                            []
                        ),

                    "benefits":
                        scheme.benefits,

                    "documents_required":
                        scheme.documents_required,

                    "how_to_apply":
                        scheme.how_to_apply,

                    "official_url":
                        scheme.official_link
                }
            )


        # ==================================================
        # STEP 14 — Return complete result
        # ==================================================

        return {
            "response_type": "results",

            "message": final_message,

            "profile": self._clean_profile(),

            "missing_information": [],

            "schemes": scheme_results
        }


    def _clean_profile(self) -> dict:
        """
        Remove internal conversation flags before
        returning the profile to the API.
        """

        return {
            key: value
            for key, value in self.session_profile.items()
            if not key.startswith("_")
        }