import pytest
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.models.scheme import Scheme
from backend.rag.vector_store import index_schemes, reset_index
from backend.rag.retriever import retrieve_relevant_schemes

@pytest.fixture(scope="module")
def setup_schemes():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'schemes.json')
    with open(path, 'r') as f:
        data = json.load(f)
    
    schemes = [Scheme(**item) for item in data]
    
    # reset and index
    reset_index()
    index_schemes(schemes)
    
    return schemes

def test_rag_agriculture(setup_schemes):
    """Test 1: Farmer querying financial assistance."""
    query = "I am a farmer and need financial assistance for agriculture."
    
    retrieved = retrieve_relevant_schemes(query, setup_schemes, top_k=2)
    
    retrieved_ids = [r["id"] for r in retrieved]
    assert "SCH001" in retrieved_ids or "SCH002" in retrieved_ids

def test_rag_education(setup_schemes):
    """Test 2: Financial assistance for college education."""
    query = "I am looking for financial assistance for my college education."
    retrieved = retrieve_relevant_schemes(query, setup_schemes, top_k=2)
    
    retrieved_ids = [r["id"] for r in retrieved]
    assert "SCH003" in retrieved_ids or "SCH004" in retrieved_ids

def test_rag_healthcare(setup_schemes):
    """Test 3: Healthcare help."""
    query = "I need government help for healthcare."
    retrieved = retrieve_relevant_schemes(query, setup_schemes, top_k=2)
    
    retrieved_ids = [r["id"] for r in retrieved]
    assert "SCH007" in retrieved_ids # Ayushman Bharat

def test_inactive_schemes_ignored(setup_schemes):
    """Test 4: Verify inactive schemes not indexed."""
    inactive_scheme = Scheme(
        id="SCH999",
        name="Inactive Scheme",
        category="General",
        state="All",
        description="Testing inactive",
        eligibility={"min_age": None, "max_age": None, "max_income": None, "occupations": [], "education": [], "categories": [], "min_land_acres": None, "max_land_acres": None},
        target_beneficiaries=["all"],
        benefits=["None"],
        documents_required=["None"],
        how_to_apply="None",
        official_link="None",
        status="inactive"
    )
    # Re-index with this scheme appended
    index_schemes([inactive_scheme])
    
    query = "Inactive Scheme"
    retrieved = retrieve_relevant_schemes(query, [inactive_scheme], top_k=1)
    assert len(retrieved) == 0

def test_restricted_to_candidates(setup_schemes):
    """Test 5: Verify retrieval only searches within candidates."""
    query = "I need government help for healthcare."
    
    # Pass an empty candidate list
    retrieved = retrieve_relevant_schemes(query, [], top_k=5)
    assert len(retrieved) == 0
    
    # Pass only education schemes as candidates
    education_schemes = [s for s in setup_schemes if s.category == "Education"]
    retrieved = retrieve_relevant_schemes(query, education_schemes, top_k=5)
    retrieved_ids = [r["id"] for r in retrieved]
    
    # Should not retrieve SCH007 (Healthcare) because it's not in candidates
    assert "SCH007" not in retrieved_ids
