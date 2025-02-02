FROM nvidia/cuda:12.0.0-base-ubuntu22.04

RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /app

# Copy .env file first to use during build
COPY .env .env
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

# Pre-download model during build otherwise it will be downloaded at runtime at make cloud run fail
RUN python3 -c "from transformers import AutoTokenizer, AutoModelForCausalLM; \
    from dotenv import load_dotenv; \
    load_dotenv(); \
    import os; \
    token = os.getenv('HUGGINGFACE_TOKEN'); \
    model_name='deepseek-ai/deepseek-r1-distill-qwen-7b'; \
    AutoTokenizer.from_pretrained(model_name, token=token); \
    AutoModelForCausalLM.from_pretrained(model_name, token=token)"

# Default port for documentation, actual port set by environment variable
EXPOSE 8080

CMD uvicorn src.main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8080}