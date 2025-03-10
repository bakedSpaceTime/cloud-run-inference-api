import sys
import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Try to load from .env file if it exists, otherwise use environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # Use environment variables directly

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log startup information
logger.info("Starting application...")

app = FastAPI()

# Get port from environment variable or use default
PORT = int(os.environ.get("PORT", 8080))
logger.info(f"Configured to listen on port {PORT}")
# Default to "0.0.0.0" for Docker/Cloud Run, but allow override
HOST = os.getenv("HOST", "0.0.0.0")

# Ensure the model name is correct from Hugging Face or Vertex AI
model_path = "/app/hf/models/deepseek-r1-distill-qwen-7b"
# Initialize these at module level but load them lazily
tokenizer = None
model = None


def load_model():
    """Load model and tokenizer if not already loaded"""
    global tokenizer, model
    if tokenizer is None or model is None:
        try:
            logger.info("Loading model and tokenizer...")
            # Load from cache (model should have been downloaded during build)
            tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
            model = AutoModelForCausalLM.from_pretrained(
                model_path, local_files_only=True, torch_dtype=torch.float16
            )
            logger.info("Model loaded successfully!")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise


class InferenceRequest(BaseModel):
    prompt: str
    max_tokens: int = 512


@app.post("/v1/inference")
async def inference(request: InferenceRequest):
    try:
        load_model()  # Ensure model is loaded
        inputs = tokenizer(request.prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(inputs.input_ids, max_new_tokens=request.max_tokens)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"response": response}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Inference failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to generate response: {str(e)}"
        )


@app.get("/v1/sanity-check")
async def sanity_check():
    logger.info("Sanity check endpoint called")
    return {"response": "Sanity check passed!"}


@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
