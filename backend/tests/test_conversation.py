import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from unittest.mock import patch
from backend.llm.profile_extractor import extract_profile_from_message
from backend.conversation.missing_info import determine_missing_important_info
from backend.conversation.conversation_manager import ConversationManager
from backend.models.scheme import Scheme

def test_extract_farmer():
    """Test 1: User message extraction"""
    with patch('backend.llm.profile_extractor.generate_structured_json') as mock_gen:
        mock_gen.return_value = {
            "state": "Andhra Pradesh",
            "occupation": "Farmer",
            "land_acres": 2.0,
            "age": None,
            "annual_income": None,
            "education": None,
            "category": None,
            "gender": None,
            "beneficiary_for": None,
            "user_intent": "agriculture_support"
        }
        
        msg = "I am a farmer from AP with 2 acres of land."
        profile = extract_profile_from_message(msg)
        
        assert profile["state"] == "Andhra Pradesh"
        assert profile["occupation"] == "Farmer"
        assert profile["land_acres"] == 2.0
        assert profile.get("age") is None

def test_merge_profile():
    """Test 2: Merge new info with existing profile"""
    with patch('backend.llm.profile_extractor.generate_structured_json') as mock_gen:
        mock_gen.return_value = {
            "age": 35,
            "annual_income": 200000,
            "state": None,
            "occupation": None,
            "land_acres": None,
            "education": None,
            "category": None,
            "gender": None,
            "beneficiary_for": None,
            "user_intent": None
        }
        
        existing = {
            "state": "Andhra Pradesh",
            "occupation": "Farmer",
            "land_acres": 2.0
        }
        
        profile = extract_profile_from_message("I am 35 and earn 2 lakh per year.", existing)
        
        assert profile["age"] == 35
        assert profile["annual_income"] == 200000
        # Existing values must remain unchanged
        assert profile["state"] == "Andhra Pradesh"
        assert profile["occupation"] == "Farmer"

def test_missing_info_agriculture():
    """Test 3: Missing information detection for agriculture query."""
    profile = {
        "user_intent": "agriculture_support",
        "state": "Andhra Pradesh",
        "occupation": "Farmer"
    }
    
    missing = determine_missing_important_info(profile)
    assert "land_acres" in missing
    assert "annual_income" in missing
    assert "state" not in missing
    
def test_conversation_manager_fallback():
    """Test 4 & 5: Complete profile triggers pipeline & Fallback logic works"""
    dummy_scheme = Scheme(
        id="SCH001",
        name="PM-KISAN",
        category="Agriculture",
        state="All",
        description="Test",
        eligibility={"min_age": None, "max_age": None, "max_income": None, "occupations": ["Farmer"], "education": [], "categories": [], "min_land_acres": None, "max_land_acres": 5.0},
        target_beneficiaries=["farmer", "all"],
        benefits=["None"],
        documents_required=["None"],
        how_to_apply="None",
        official_link="pmkisan.gov.in",
        status="active"
    )
    
    manager = ConversationManager([dummy_scheme])
    
    with patch('backend.conversation.conversation_manager.extract_profile_from_message') as mock_extract, \
         patch('backend.llm.response_generator.generate_text', return_value=None), \
         patch('backend.conversation.conversation_manager.retrieve_relevant_schemes') as mock_retrieve:
        
        mock_extract.return_value = {
            "age": 35,
            "state": "Andhra Pradesh",
            "occupation": "Farmer",
            "annual_income": 200000,
            "land_acres": 2.0,
            "user_intent": "agriculture_support"
        }
        
        mock_retrieve.return_value = [{"id": "SCH001", "name": "PM-KISAN", "document": "test", "distance": 0.5}]
        
        response = manager.process_message("Show me schemes.")
        
        assert "PM-KISAN" in response
        assert "Status: LIKELY_ELIGIBLE" in response
        assert "Official Source: pmkisan.gov.in" in response
