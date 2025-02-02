import pytest
import os
import sys
from pathlib import Path

# Add the project root to Python path to help with imports
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    """Setup environment variables for testing"""
    # Set test environment variables
    test_env = {
        "HUGGINGFACE_TOKEN": "test_token",
        "PORT": "8080",
        "HOST": "0.0.0.0",
    }
    
    # Use monkeypatch to set environment variables for tests
    for key, value in test_env.items():
        monkeypatch.setenv(key, value) 