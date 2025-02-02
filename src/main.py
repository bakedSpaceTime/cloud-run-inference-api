import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load environment variables from .env file
load_dotenv()

app = FastAPI()
# Ensure the model name is correct from Hugging Face
model_name = "deepseek-ai/deepseek-r1-distill-qwen-7b"
auth_token = os.getenv("HUGGINGFACE_TOKEN")
if not auth_token:
    raise ValueError("HUGGINGFACE_TOKEN not found in environment variables")

tokenizer = AutoTokenizer.from_pretrained(model_name, token=auth_token)
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