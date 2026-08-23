import re
from typing import Any, Dict

from backend.llm.gemini_client import generate_structured_json


VALID_FIELDS = {
    "age",
    "state",
    "occupation",
    "annual_income",
    "education",
    "category",
    "land_acres",
    "gender",
    "beneficiary_for",
    "user_intent",
}


def normalize_state(value: str) -> str:
    if not value:
        return value

    value = value.strip().lower()

    state_map = {
        "ap": "Andhra Pradesh",
        "andhra": "Andhra Pradesh",
        "andhra pradesh": "Andhra Pradesh",

        "ts": "Telangana",
        "telangana": "Telangana",

        "tn": "Tamil Nadu",
        "tamil nadu": "Tamil Nadu",

        "ka": "Karnataka",
        "karnataka": "Karnataka",

        "kl": "Kerala",
        "kerala": "Kerala",

        "mh": "Maharashtra",
        "maharashtra": "Maharashtra",

        "up": "Uttar Pradesh",
        "uttar pradesh": "Uttar Pradesh",

        "mp": "Madhya Pradesh",
        "madhya pradesh": "Madhya Pradesh",

        "dl": "Delhi",
        "delhi": "Delhi",

        "odisha": "Odisha",
        "orissa": "Odisha",

        "west bengal": "West Bengal",
        "wb": "West Bengal",

        "bihar": "Bihar",
        "br": "Bihar",

        "rajasthan": "Rajasthan",
        "rj": "Rajasthan",

        "gujarat": "Gujarat",
        "gj": "Gujarat",

        "punjab": "Punjab",
        "pb": "Punjab",

        "haryana": "Haryana",
        "hr": "Haryana",

        "assam": "Assam",

        "jharkhand": "Jharkhand",

        "chhattisgarh": "Chhattisgarh",

        "goa": "Goa",
    }

    return state_map.get(value, value.title())


def parse_number(value: str):
    """
    Convert values like:

    150000
    1.5 lakh
    2 lakhs
    1 crore
    50 thousand
    """

    if value is None:
        return None

    value = str(value).lower().replace(",", "").strip()

    number_match = re.search(r"(\d+(?:\.\d+)?)", value)

    if not number_match:
        return None

    number = float(number_match.group(1))

    if "crore" in value:
        number *= 10000000

    elif "lakh" in value:
        number *= 100000

    elif "thousand" in value or re.search(r"\b\d+(?:\.\d+)?k\b", value):
        number *= 1000

    return number


def local_extract_profile(message: str) -> Dict[str, Any]:
    """
    Rule-based fallback extraction.

    This works together with Gemini extraction.
    Local rules are especially useful for simple structured facts such as:
    - age
    - state
    - occupation
    - income
    - land
    """

    profile = {}
    text = message.lower().strip()

    # ==================================================
    # AGE
    # ==================================================

    age_patterns = [
        # I am 20 years old
        r"\bi am (?:a\s+)?(\d{1,3})\s+years?\s+old\b",

        # I'm 20 years old
        r"\bi['’]m (?:a\s+)?(\d{1,3})\s+years?\s+old\b",

        # I am 20 year old farmer
        r"\bi am (?:a\s+)?(\d{1,3})\s+year\s+old\b",

        # 20 year old / 20 years old
        r"\b(\d{1,3})\s+years?\s+old\b",

        # age is 20
        r"\bage\s*(?:is|:)?\s*(\d{1,3})\b",

        # my age is 20
        r"\bmy age\s*(?:is|:)?\s*(\d{1,3})\b",

        # I am 20
        r"\bi am (?:a\s+)?(\d{1,3})\b",

        # I'm 20
        r"\bi['’]m (?:a\s+)?(\d{1,3})\b",
    ]

    for pattern in age_patterns:
        match = re.search(pattern, text)

        if match:
            age = int(match.group(1))

            if 0 < age < 120:
                profile["age"] = age
                break

    # ==================================================
    # STATE
    # ==================================================

    states = {
        "andhra pradesh": "Andhra Pradesh",
        "andhra": "Andhra Pradesh",
        "telangana": "Telangana",
        "tamil nadu": "Tamil Nadu",
        "karnataka": "Karnataka",
        "kerala": "Kerala",
        "maharashtra": "Maharashtra",
        "uttar pradesh": "Uttar Pradesh",
        "madhya pradesh": "Madhya Pradesh",
        "rajasthan": "Rajasthan",
        "gujarat": "Gujarat",
        "bihar": "Bihar",
        "odisha": "Odisha",
        "west bengal": "West Bengal",
        "punjab": "Punjab",
        "haryana": "Haryana",
        "assam": "Assam",
        "jharkhand": "Jharkhand",
        "chhattisgarh": "Chhattisgarh",
        "goa": "Goa",
        "delhi": "Delhi",
    }

    for state_key, state_name in states.items():
        if re.search(rf"\b{re.escape(state_key)}\b", text):
            profile["state"] = state_name
            break

    # Short forms
    if (
        re.search(r"\bfrom ap\b", text)
        or re.search(r"\bin ap\b", text)
        or re.search(r"\bstate is ap\b", text)
        or re.search(r"\bi live in ap\b", text)
    ):
        profile["state"] = "Andhra Pradesh"

    elif (
        re.search(r"\bfrom ts\b", text)
        or re.search(r"\bin ts\b", text)
        or re.search(r"\bstate is ts\b", text)
    ):
        profile["state"] = "Telangana"

    # ==================================================
    # LAND
    # ==================================================

    land_patterns = [
        r"(?:own|owns|owned|have|having)\s*(\d+(?:\.\d+)?)\s*acres?\b",
        r"(\d+(?:\.\d+)?)\s*acres?\s*(?:of\s+)?land\b",
        r"land.*?(\d+(?:\.\d+)?)\s*acres?\b",
        r"\b(\d+(?:\.\d+)?)\s*acres?\b",
    ]

    for pattern in land_patterns:
        match = re.search(pattern, text)

        if match:
            profile["land_acres"] = float(match.group(1))
            break

    # ==================================================
    # ANNUAL INCOME
    # ==================================================

    income_patterns = [
        r"(?:annual income|yearly income|income)\s*(?:is|of|:)?\s*(?:₹|rs\.?|inr)?\s*([\d,.]+(?:\s*(?:lakh|lakhs|crore|crores|thousand))?)",

        r"(?:earn|earning)\s*(?:₹|rs\.?|inr)?\s*([\d,.]+(?:\s*(?:lakh|lakhs|crore|crores|thousand))?)",

        r"(?:my income is|income is)\s*(?:₹|rs\.?|inr)?\s*([\d,.]+(?:\s*(?:lakh|lakhs|crore|crores|thousand))?)",
    ]

    for pattern in income_patterns:
        match = re.search(pattern, text)

        if match:
            income_text = match.group(1)
            income = parse_number(income_text)

            if income is not None:
                profile["annual_income"] = income
                break

    # ==================================================
    # OCCUPATION
    # ==================================================

    occupation_map = {
        "government employee": "Government Employee",
        "private employee": "Private Employee",
        "self-employed": "Self Employed",
        "self employed": "Self Employed",
        "agriculturist": "Farmer",
        "farmer": "Farmer",
        "agriculture": "Farmer",
        "student": "Student",
        "employee": "Employee",
        "businessman": "Business Owner",
        "business": "Business Owner",
        "labourer": "Labourer",
        "laborer": "Labourer",
        "unemployed": "Unemployed",
    }

    for keyword, occupation in occupation_map.items():
        if re.search(rf"\b{re.escape(keyword)}\b", text):
            profile["occupation"] = occupation
            break

    # ==================================================
    # GENDER
    # ==================================================

    if re.search(r"\bfemale\b", text):
        profile["gender"] = "Female"

    elif re.search(r"\bmale\b", text):
        profile["gender"] = "Male"

    elif re.search(r"\bwoman\b|\bgirl\b", text):
        profile["gender"] = "Female"

    elif re.search(r"\bman\b|\bboy\b", text):
        profile["gender"] = "Male"

    # ==================================================
    # CATEGORY
    # ==================================================

    category_map = {
        "general": "General",
        "obc": "OBC",
        "bc": "BC",
        "scheduled caste": "SC",
        "sc": "SC",
        "scheduled tribe": "ST",
        "st": "ST",
        "ews": "EWS",
    }

    for keyword, category in category_map.items():
        if re.search(rf"\b{re.escape(keyword)}\b", text):
            profile["category"] = category
            break

    # ==================================================
    # EDUCATION
    # ==================================================

    education_patterns = {
        "b.tech": "B.Tech",
        "btech": "B.Tech",
        "engineering": "Engineering",
        "postgraduate": "Postgraduate",
        "graduate": "Graduate",
        "degree": "Graduate",
        "intermediate": "Intermediate",
        "12th": "12th",
        "10th": "10th",
        "school": "School",
    }

    for keyword, education in education_patterns.items():
        if keyword in text:
            profile["education"] = education
            break

    # ==================================================
    # USER INTENT
    # ==================================================

    if any(
        phrase in text
        for phrase in [
            "scheme",
            "eligible",
            "eligibility",
            "government help",
            "government benefit",
            "subsidy",
            "financial assistance",
            "apply for",
        ]
    ):
        profile["user_intent"] = "Find eligible government schemes"

    return profile


def clean_extracted_data(data: Any) -> Dict[str, Any]:
    """
    Keep only valid non-null profile fields.
    """

    if not isinstance(data, dict):
        return {}

    cleaned = {}

    for key, value in data.items():
        if key not in VALID_FIELDS:
            continue

        if value is None:
            continue

        if isinstance(value, str) and not value.strip():
            continue

        cleaned[key] = value

    # Normalize state
    if "state" in cleaned:
        cleaned["state"] = normalize_state(str(cleaned["state"]))

    # Convert age
    if "age" in cleaned:
        try:
            age = int(float(cleaned["age"]))

            if 0 < age < 120:
                cleaned["age"] = age
            else:
                cleaned.pop("age", None)

        except (ValueError, TypeError):
            cleaned.pop("age", None)

    # Convert income
    if "annual_income" in cleaned:
        try:
            if isinstance(cleaned["annual_income"], str):
                income = parse_number(cleaned["annual_income"])
            else:
                income = float(cleaned["annual_income"])

            if income is not None and income >= 0:
                cleaned["annual_income"] = income
            else:
                cleaned.pop("annual_income", None)

        except (ValueError, TypeError):
            cleaned.pop("annual_income", None)

    # Convert land
    if "land_acres" in cleaned:
        try:
            land = float(cleaned["land_acres"])

            if land >= 0:
                cleaned["land_acres"] = land
            else:
                cleaned.pop("land_acres", None)

        except (ValueError, TypeError):
            cleaned.pop("land_acres", None)

    return cleaned


def extract_profile_from_message(
    user_message: str,
    existing_profile: dict = None
) -> dict:
    """
    Extract citizen profile information.

    Strategy:
    1. Try Gemini structured extraction.
    2. Use local extraction as fallback.
    3. Merge with the existing conversation profile.
    """

    if existing_profile is None:
        existing_profile = {}

    # ==================================================
    # GEMINI EXTRACTION
    # ==================================================

    prompt = f"""
You are extracting structured information for an Indian government
scheme eligibility assistant.

Extract ONLY information explicitly present in the user's message.

Return a JSON object with exactly these fields:

{{
  "age": null,
  "state": null,
  "occupation": null,
  "annual_income": null,
  "education": null,
  "category": null,
  "land_acres": null,
  "gender": null,
  "beneficiary_for": null,
  "user_intent": null
}}

Normalization rules:

- AP -> Andhra Pradesh
- TS -> Telangana
- 2 acres -> 2.0
- two lakh -> 200000
- 1.5 lakhs -> 150000
- farmer -> Farmer
- student -> Student
- "20 year old" -> age 20
- "20 years old" -> age 20
- "I am 20" -> age 20

Do not invent information.
Use null for missing fields.

User message:
"{user_message}"
"""

    gemini_data = {}

    try:
        result = generate_structured_json(prompt)
        gemini_data = clean_extracted_data(result)

    except Exception:
        gemini_data = {}

    # ==================================================
    # LOCAL EXTRACTION
    # ==================================================

    local_data = local_extract_profile(user_message)

    # ==================================================
    # MERGE
    # ==================================================

    merged_profile = existing_profile.copy()

    # Gemini data has priority
    for key, value in gemini_data.items():
        if value is not None:
            merged_profile[key] = value

    # Local extraction fills missing fields
    for key, value in local_data.items():
        if value is not None:
            if key not in merged_profile or merged_profile[key] is None:
                merged_profile[key] = value

    return merged_profile