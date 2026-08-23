import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_get_schemes():
    response = client.get("/api/schemes")
    assert response.status_code == 200
    schemes = response.json()
    assert isinstance(schemes, list)
    
    if len(schemes) > 0:
        scheme = schemes[0]
        assert "scheme_id" in scheme
        assert "scheme_name" in scheme
        assert "category" in scheme
        assert "status" in scheme
        assert scheme["status"].lower() == "active"
