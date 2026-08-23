import pytest
import os
import sys
import json

# Ensure backend can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.models.citizen import CitizenProfile
from backend.models.scheme import Scheme
from backend.eligibility.eligibility_engine import EligibilityEngine
from backend.services.scheme_filter import filter_schemes

def load_schemes():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'schemes.json')
    with open(path, 'r') as f:
        data = json.load(f)
        return [Scheme(**item) for item in data]

def test_farmer_ap_eligible():
    """
    Test 1 (Original):
    Farmer from Andhra Pradesh
    """
    schemes = load_schemes()
    citizen = CitizenProfile(
        age=35,
        state="Andhra Pradesh",
        occupation="Farmer",
        annual_income=200000,
        land_acres=2
    )
    
    pm_kisan = next(s for s in schemes if s.id == "SCH001")
    ap_ysr = next(s for s in schemes if s.id == "SCH002")
    
    result_pm = EligibilityEngine.check_eligibility(citizen, pm_kisan)
    assert result_pm["eligibility_status"] == "LIKELY_ELIGIBLE"
    
    result_ap = EligibilityEngine.check_eligibility(citizen, ap_ysr)
    assert result_ap["eligibility_status"] == "LIKELY_ELIGIBLE"

def test_student_ap_missing_category():
    """
    Test 2 (Original):
    Student from AP
    """
    schemes = load_schemes()
    citizen = CitizenProfile(
        age=22,
        state="Andhra Pradesh",
        occupation="Student",
        annual_income=150000
    )
    
    jagananna = next(s for s in schemes if s.id == "SCH004")
    res_jagananna = EligibilityEngine.check_eligibility(citizen, jagananna)
    assert res_jagananna["eligibility_status"] == "LIKELY_ELIGIBLE"
    
    nsp = next(s for s in schemes if s.id == "SCH003")
    res_nsp = EligibilityEngine.check_eligibility(citizen, nsp)
    assert res_nsp["eligibility_status"] == "POSSIBLY_ELIGIBLE" 

def test_missing_income_info():
    """
    Test 3 (Original):
    Missing income
    """
    schemes = load_schemes()
    citizen = CitizenProfile(
        age=30,
        state="Telangana"
    )
    
    ayushman = next(s for s in schemes if s.id == "SCH007")
    res = EligibilityEngine.check_eligibility(citizen, ayushman)
    assert res["eligibility_status"] == "MORE_INFORMATION_REQUIRED"
    assert "annual_income" in res["missing_information"]

def test_fails_age_requirement():
    """
    Test 4 (Original):
    Fails age
    """
    schemes = load_schemes()
    citizen = CitizenProfile(
        age=15,
        state="Maharashtra",
        occupation="Self-employed"
    )
    
    mudra = next(s for s in schemes if s.id == "SCH005")
    res = EligibilityEngine.check_eligibility(citizen, mudra)
    assert res["eligibility_status"] == "NOT_ELIGIBLE"
    assert any("age requirement" in cond for cond in res["failed_conditions"])

# --- NEW TESTS (Task 7) ---

def test_farmer_male_relevance():
    """Test 1: 35-year-old male farmer..."""
    schemes = load_schemes()
    citizen = CitizenProfile(
        age=35,
        state="Andhra Pradesh",
        occupation="Farmer",
        annual_income=200000,
        land_acres=2,
        gender="Male",
        beneficiary_for="self"
    )
    
    filtered = filter_schemes(schemes, citizen)
    scheme_ids = [s.id for s in filtered]
    
    # Should not include female-only schemes like Sukanya (SCH008) and Janani (SCH009)
    assert "SCH008" not in scheme_ids
    assert "SCH009" not in scheme_ids
    
    # Should include PM-KISAN (SCH001)
    assert "SCH001" in scheme_ids

def test_female_student_scholarship():
    """Test 2: 22-year-old female student..."""
    schemes = load_schemes()
    citizen = CitizenProfile(
        age=22,
        state="Andhra Pradesh",
        occupation="Student",
        annual_income=150000,
        gender="Female",
        beneficiary_for="self",
        user_intent="scholarship"
    )
    filtered = filter_schemes(schemes, citizen)
    
    # Check relevance ranking
    # Jagananna (SCH004) should be HIGHLY_RELEVANT due to "scholarship" intent and "Education" category
    jagananna = next(s for s in filtered if s.id == "SCH004")
    res = EligibilityEngine.check_eligibility(citizen, jagananna)
    assert res["relevance_status"] == "HIGHLY_RELEVANT"

def test_parent_for_daughter():
    """Test 3: Parent searching for daughter"""
    schemes = load_schemes()
    citizen = CitizenProfile(
        gender="Male",
        beneficiary_for="daughter"
    )
    filtered = filter_schemes(schemes, citizen)
    scheme_ids = [s.id for s in filtered]
    
    # Sukanya Samriddhi Yojana (SCH008) is a girl_child scheme
    assert "SCH008" in scheme_ids
    
    res = EligibilityEngine.check_eligibility(citizen, next(s for s in schemes if s.id == "SCH008"))
    assert res["relevance_status"] == "HIGHLY_RELEVANT"

def test_missing_gender_info():
    """Test 4: Missing gender or beneficiary info."""
    schemes = load_schemes()
    citizen = CitizenProfile(
        age=30
    )
    filtered = filter_schemes(schemes, citizen)
    scheme_ids = [s.id for s in filtered]
    
    # Female specific schemes should not be aggressively removed if gender is missing
    assert "SCH008" in scheme_ids
    assert "SCH009" in scheme_ids
