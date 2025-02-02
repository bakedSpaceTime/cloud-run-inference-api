import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load environment variables from .env file
load_dotenv()

app = FastAPI()
# Get port from environment variable or use default
PORT = int(os.getenv("PORT", "8080"))
# Default to "0.0.0.0" for Docker/Cloud Run, but allow override
HOST = os.getenv("HOST", "0.0.0.0")

# Ensure the model name is correct from Hugging Face
model_name = "deepseek-ai/deepseek-r1-distill-qwen-7b"
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
if not auth_token:
    raise ValueError("HUGGINGFACE_TOKEN not found in environment variables")

tokenizer = AutoTokenizer.from_pretrained(model_name, token=HUGGINGFACE_TOKEN)
model = AutoModelForCausalLM.from_pretrained(
    model_name, 
    token=auth_token,
    torch_dtype=torch.float16
)
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
    return {"response": "Sanity check passed!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
