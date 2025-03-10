FROM us-docker.pkg.dev/deeplearning-platform-release/gcr.io/huggingface-text-generation-inference-cu121.2-2.ubuntu2204.py310

# Accept HF_TOKEN as a build argument
ARG HF_TOKEN
ENV HF_TOKEN=${HF_TOKEN}

WORKDIR /app
COPY . .

# Install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# Download the depseek model using huggingface-cli
RUN huggingface-cli download deepseek-ai/deepseek-r1-distill-qwen-7b --local-dir /app/hf/models/deepseek-r1-distill-qwen-7b --cache-dir /app/hf/cache

EXPOSE 8080
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
