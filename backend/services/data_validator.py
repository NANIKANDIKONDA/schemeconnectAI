import json
import os
from typing import List, Tuple

from backend.models.scheme import Scheme


DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "schemes.json"
)


def load_and_validate_schemes() -> Tuple[List[Scheme], List[dict]]:
    """
    Load schemes.json and validate every scheme using the Pydantic Scheme model.

    Returns:
        valid_schemes: List of validated Scheme objects
        errors: List of validation errors
    """

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"schemes.json not found at: {DATA_PATH}"
        )

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            "schemes.json must contain a JSON array of scheme objects."
        )

    valid_schemes = []
    errors = []

    seen_ids = set()

    for index, scheme_data in enumerate(data):

        try:
            scheme = Scheme(**scheme_data)

            # Check duplicate scheme IDs
            if scheme.id in seen_ids:
                errors.append({
                    "index": index,
                    "scheme_id": scheme.id,
                    "error": "Duplicate scheme_id found"
                })
                continue

            seen_ids.add(scheme.id)

            # Basic validation
            if not scheme.name.strip():
                errors.append({
                    "index": index,
                    "scheme_id": scheme.id,
                    "error": "Scheme name cannot be empty"
                })
                continue

            if not scheme.description.strip():
                errors.append({
                    "index": index,
                    "scheme_id": scheme.id,
                    "error": "Scheme description cannot be empty"
                })
                continue

            if not scheme.category.strip():
                errors.append({
                    "index": index,
                    "scheme_id": scheme.id,
                    "error": "Scheme category cannot be empty"
                })
                continue

            valid_schemes.append(scheme)

        except Exception as error:
            errors.append({
                "index": index,
                "scheme_id": scheme_data.get(
                    "scheme_id",
                    "UNKNOWN"
                ),
                "error": str(error)
            })

    return valid_schemes, errors


def print_validation_report():
    """
    Print a readable validation report.
    """

    valid_schemes, errors = load_and_validate_schemes()

    print("\n" + "=" * 70)
    print("SCHEMECONNECT AI - DATASET VALIDATION REPORT")
    print("=" * 70)

    print(f"\nValid schemes: {len(valid_schemes)}")
    print(f"Invalid schemes: {len(errors)}")

    if errors:
        print("\nVALIDATION ERRORS")
        print("-" * 70)

        for error in errors:
            print(
                f"\nIndex: {error['index']}"
            )
            print(
                f"Scheme ID: {error['scheme_id']}"
            )
            print(
                f"Error: {error['error']}"
            )

    else:
        print("\nAll schemes passed validation successfully.")

    print("\n" + "=" * 70)

    return valid_schemes, errors


if __name__ == "__main__":
    print_validation_report()