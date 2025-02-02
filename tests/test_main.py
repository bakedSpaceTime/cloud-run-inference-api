import pytest
from fastapi.testclient import TestClient
import sys
from unittest.mock import MagicMock, patch
from src.main import app, load_model

# Mock dotenv before importing main
sys.modules['dotenv'] = MagicMock()
sys.modules['python-dotenv'] = MagicMock()

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

@pytest.mark.skip(reason="Not implemented yet")
@patch('src.main.AutoTokenizer')
@patch('src.main.AutoModelForCausalLM')
def test_inference_endpoint_success(mock_auto_model, mock_tokenizer):
    """Test successful model inference"""
    # Setup mocks
    mock_tokenizer_instance = MagicMock()
    mock_model_instance = MagicMock()
    mock_device = MagicMock()
    
    # Configure mock tokenizer
    mock_tokenizer.from_pretrained.return_value = mock_tokenizer_instance
    mock_tokenizer_instance.return_value = MagicMock()
    mock_tokenizer_instance.__call__.return_value = MagicMock(input_ids=MagicMock())
    mock_tokenizer_instance.decode.return_value = "Mocked response"
    
    # Configure mock model
    mock_auto_model.from_pretrained.return_value = mock_model_instance
    mock_model_instance.device = mock_device
    mock_model_instance.generate.return_value = [MagicMock()]

    with patch.dict('os.environ', {'HUGGINGFACE_TOKEN': 'test_token'}):
        response = client.post(
            "/v1/inference",
            json={"prompt": "Test prompt", "max_tokens": 10}
        )

    assert response.status_code == 200
    assert "response" in response.json()

def test_inference_missing_token():
    """Test inference fails when HUGGINGFACE_TOKEN is missing"""
    with patch.dict('os.environ', clear=True):  # Clear environment variables
        response = client.post(
            "/v1/inference",
            json={"prompt": "Test prompt", "max_tokens": 10}
        )
        assert response.status_code == 500
        assert "HUGGINGFACE_TOKEN not found" in response.json()["detail"]

@patch('src.main.AutoTokenizer')
@patch('src.main.AutoModelForCausalLM')
def test_model_load_error(mock_auto_model, mock_tokenizer):
    """Test handling of model loading errors"""
    mock_tokenizer.from_pretrained.side_effect = Exception("Model loading failed")
    
    with patch.dict('os.environ', {'HUGGINGFACE_TOKEN': 'test_token'}):
        response = client.post(
            "/v1/inference",
            json={"prompt": "Test prompt", "max_tokens": 10}
        )
    
    assert response.status_code == 500
    assert "Model loading failed" in response.json()["detail"]

@pytest.mark.skip(reason="Need to implement validation")
def test_inference_validation():
    """Test input validation for inference endpoint"""
    # Test missing prompt
    response = client.post("/v1/inference", json={"max_tokens": 10})
    assert response.status_code == 422

    # Test negative max_tokens
    with patch.dict('os.environ', {'HUGGINGFACE_TOKEN': 'test_token'}):
        response = client.post(
            "/v1/inference", 
            json={"prompt": "test", "max_tokens": -1}
        )
        assert response.status_code == 422 