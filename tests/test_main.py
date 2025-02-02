import pytest
from fastapi.testclient import TestClient
import sys
from unittest.mock import MagicMock

# Mock dotenv before importing main
sys.modules['dotenv'] = MagicMock()
sys.modules['python-dotenv'] = MagicMock()
from src.main import app

client = TestClient(app)

def test_sanity_check():
    """Test the sanity check endpoint returns expected response"""
    response = client.get("/v1/sanity-check")
    assert response.status_code == 200
    assert response.json() == {"response": "Sanity check passed!"}

def test_sanity_check_wrong_method():
    """Test that using wrong HTTP method returns 405"""
    response = client.post("/v1/sanity-check")
    assert response.status_code == 405 