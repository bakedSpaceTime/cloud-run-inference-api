# Stage 1: Download model
FROM nvidia/cuda:12.0.0-base-ubuntu22.04 AS model-downloader

# Define build argument for Hugging Face token
ARG HUGGINGFACE_TOKEN

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /model
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Download model using the provided token
RUN python3 -c "\
    from transformers import AutoTokenizer, AutoModelForCausalLM; \
    import os; \
    model_name='deepseek-ai/deepseek-r1-distill-qwen-7b'; \
    cache_dir='/model/cache'; \
    AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir, token='${HUGGINGFACE_TOKEN}'); \
    AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir, token='${HUGGINGFACE_TOKEN}')"

# Stage 2: Final image
FROM nvidia/cuda:12.0.0-base-ubuntu22.04

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

# Copy the downloaded model from the previous stage
COPY --from=model-downloader /model/cache /root/.cache/huggingface

# Default port for documentation, actual port set by environment variable
EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]