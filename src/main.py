from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


app = FastAPI()
model_name = "deepseek-ai/deepseek-r1-distill-7b"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)
class InferenceRequest(BaseModel):
    prompt: str
    max_tokens: int = 512
@app.post("/v1/inference")
async def inference(request: InferenceRequest):
    inputs = tokenizer(request.prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(inputs.input_ids, max_new_tokens=request.max_tokens)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"response": response}