import sys
import os
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from dotenv import load_dotenv
load_dotenv()

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


# Ensure the model name is correct from Hugging Face
model_name = "deepseek-ai/deepseek-r1-distill-qwen-7b"
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
if not HUGGINGFACE_TOKEN:
    raise ValueError("HUGGINGFACE_TOKEN not found in environment variables")

try:
    logger.info("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=HUGGINGFACE_TOKEN)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        token=HUGGINGFACE_TOKEN,
        torch_dtype=torch.float16
    )
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    sys.exit(1)


class InferenceRequest(BaseModel):
    prompt: str
    max_tokens: int = 512
    
@app.post("/v1/inference")
async def inference(request: InferenceRequest):
    inputs = tokenizer(request.prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(inputs.input_ids, max_new_tokens=request.max_tokens)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"response": response}

@app.get("/v1/sanity-check")
async def sanity_check():
    logger.info("Sanity check endpoint called")
    return {"response": "Sanity check passed!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
