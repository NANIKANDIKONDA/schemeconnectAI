import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.main import app
import uuid

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "SchemeConnect AI",
        "version": "1.0.0"
    }

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to SchemeConnect AI API",
        "docs": "/docs"
    }

@patch('backend.llm.profile_extractor.generate_structured_json')
def test_chat_first_message(mock_json):
    # Mocking Gemini extraction
    mock_json.return_value = {
        "occupation": "Farmer",
        "state": "Andhra Pradesh",
        "land_acres": 2.0
    }
    
    response = client.post("/api/chat", json={
        "message": "I am a farmer from Andhra Pradesh with 2 acres of land."
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["response_type"] in ["follow_up", "results"]
    assert data["profile"].get("occupation") == "Farmer"

@patch('backend.llm.profile_extractor.generate_structured_json')
def test_chat_multi_turn(mock_json):
    # Turn 1
    mock_json.return_value = {
        "occupation": "Farmer",
        "state": "Andhra Pradesh",
        "land_acres": 2.0
    }
    response1 = client.post("/api/chat", json={
        "message": "I am a farmer from Andhra Pradesh with 2 acres of land."
    })
    session_id = response1.json()["session_id"]
    
    # Turn 2
    mock_json.return_value = {
        "age": 35,
        "annual_income": 200000
    }
    response2 = client.post("/api/chat", json={
        "session_id": session_id,
        "message": "I am 35 years old and my annual income is 2 lakh."
    })
    
    assert response2.status_code == 200
    data2 = response2.json()
    profile = data2["profile"]
    
    # Verify previous profile information remains
    assert profile.get("occupation") == "Farmer"
    assert profile.get("state") == "Andhra Pradesh"
    assert profile.get("land_acres") == 2.0
    
    # Verify new information merges correctly
    assert profile.get("age") == 35
    assert profile.get("annual_income") == 200000
    
def test_chat_empty_message():
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 422
