FROM nvidia/cuda:12.0.0-base-ubuntu22.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# Model download with optimizations
RUN python3 -c "\
from transformers import AutoModelForCausalLM, AutoTokenizer; \
AutoTokenizer.from_pretrained('deepseek-ai/deepseek-r1-distill-qwen-7b', \
    local_files_only=False, \
    force_download=False); \
AutoModelForCausalLM.from_pretrained('deepseek-ai/deepseek-r1-distill-qwen-7b', \
    local_files_only=False, \
    force_download=False)"

EXPOSE 8080
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
