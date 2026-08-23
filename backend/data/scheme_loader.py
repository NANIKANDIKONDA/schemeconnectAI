import json
from pathlib import Path
from typing import List

from backend.models.scheme import Scheme


BASE_DIR = Path(__file__).resolve().parent
SCHEMES_PATH = BASE_DIR / "schemes.json"


def load_schemes() -> List[Scheme]:
    """
    Load all government schemes from schemes.json
    and convert them into validated Scheme objects.
    """

    if not SCHEMES_PATH.exists():
        raise FileNotFoundError(
            f"schemes.json not found at: {SCHEMES_PATH}"
        )

    with open(SCHEMES_PATH, "r", encoding="utf-8") as file:
        schemes_data = json.load(file)

    if not isinstance(schemes_data, list):
        raise ValueError(
            "schemes.json must contain a JSON array."
        )

    return [
        Scheme(**scheme)
        for scheme in schemes_data
    ]