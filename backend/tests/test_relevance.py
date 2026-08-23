from backend.models.citizen import CitizenProfile
from backend.data.scheme_loader import load_schemes
from backend.eligibility.eligibility_engine import EligibilityEngine


def test_farmer_scheme_relevance():
    schemes = load_schemes()

    citizen = CitizenProfile(
        age=20,
        state="Andhra Pradesh",
        occupation="Farmer",
        land_acres=2,
        annual_income=150000,
        user_intent="Find eligible government schemes"
    )

    print("\n" + "=" * 70)
    print("FARMER RELEVANCE TEST")
    print("=" * 70)

    expected_schemes = {
        "PM-KISAN",
        "AP YSR Rythu Bharosa"
    }

    for scheme in schemes:
        result = EligibilityEngine.check_eligibility(citizen, scheme)

        print(f"\nScheme: {scheme.name}")
        print(f"Category: {scheme.category}")
        print(f"Eligibility: {result['eligibility_status']}")
        print(f"Relevance: {result['relevance_status']}")

        if scheme.name in expected_schemes:
            assert result["relevance_status"] == "HIGHLY_RELEVANT"