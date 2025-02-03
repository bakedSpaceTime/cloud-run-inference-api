# DeepSeek Inference API

![image](https://github.com/user-attachments/assets/19a41369-2346-4bc1-9b2f-bfec5e7fdc36)

![image](https://github.com/user-attachments/assets/1d7f899e-e19e-43f5-8157-ea7c6c80dd41)

### Description

A FastAPI-based service for running inference with DeepSeek language models. This API provides a simple interface for text generation using DeepSeek's 7B model.

## Deploy DeepSeek-R1 on GCP Cloud Run!

### Why Cloud Run?

Cloud Run offers several advantages for deploying AI inference APIs, especially for early-stage projects and startups:

- **Pay-per-use pricing**: Only pay for actual compute time used, ideal for sporadic workloads
- **Auto-scaling**: Scales to zero when not in use, perfect for development and testing
- **Cost efficiency**: No need to maintain constantly running instances
- **Serverless**: Focus on code, not infrastructure
- **GPU support**: Access to T4/V100 GPUs without long-term commitments
- **Quick deployment**: From code to production in minutes

### Benefits for Early-Stage Projects

1. **Cost Optimization**

   - Zero cost when the service is idle
   - Perfect for development and testing phases
   - No minimum monthly commitments

2. **Development Flexibility**

   - Easy A/B testing of different models
   - Quick iteration and deployment
   - Simple rollback capabilities

3. **Security & Control**

   - Self-hosted solution reduces dependency on third-party services
   - Protection against service disruptions
   - Full control over model versions and updates

4. **Scalability**
   - Handles traffic spikes automatically
   - Scales down to zero during quiet periods
   - No infrastructure management overhead

## Features

- FastAPI-based REST API
- Support for DeepSeek models
- Environment-based configuration
- Token-based authentication with Hugging Face
- Docker support for containerization
- GPU acceleration support

## Prerequisites

- Python 3.11+
- Hugging Face account and API token
- GPU support (recommended)
- pip or another Python package manager

### Cost Optimization Tips

1. **Set Concurrency**

   - Adjust request concurrency to optimize resource usage
   - Example: `--concurrency 80`

2. **Memory/CPU Allocation**

   - Start with minimal resources
   - Scale up based on actual usage patterns

3. **Monitoring**
   - Use Cloud Monitoring to track usage
   - Set up alerts for unusual patterns

## Download the model During Build time rather than at runtime

This approach:

- Downloads model during build time
- Caches the model in the image
- Uses local files at runtime
- No need for token at runtime
- Faster container startup

Benefits:

- Faster cold starts
- No runtime downloads
- More reliable
- Works in airgapped environments
- Better for production
- The tradeoff is a larger container image, but the runtime benefits usually outweigh this.

## Installation

1. Clone or Fork the repository

## Usage

```python

# set up env
python3 -m venv venv

# activate the python environment
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run the FastAPI application (development)
uvicorn src.main:app --reload --port 8000

```

## Running Docker Locally

```bash


# Build with Hugging Face token
docker build -t deepseek-inference-api .

# Run the container
docker run deepseek-inference-api
```

deploy using one of these two methods:

#### Option 1: Using Cloud Build directly

```bash
# Build the image using Cloud Build
gcloud builds submit --config cloudbuild.yaml

# Then deploy the built image to Cloud Run
gcloud run deploy deepseek-service \
    --image gcr.io/$PROJECT_ID/deepseek-inference-api \
    --region us-central1 \
    --platform managed \
    --gpu \
    --memory 16Gi \
    --cpu 4 \
    --allow-unauthenticated
```

#### Option 2: Using gcloud run deploy with source

```bash
gcloud run deploy deepseek-service \
    --source . \
    --region us-central1 \
    --platform managed \
    --gpu \
    --memory 16Gi \
    --cpu 4 \
    --allow-unauthenticated
```

#### Option 3: ClickOps with Cloud Run

1. Simply go to Cloud Run on the GCP UI
2. Create a new Cloud Run Service
3. Connect to Cloud Build and to the Github Service associated with this code
4. Deploy with the Dockerfile
5. Ensure the Cloud Run Service has the same recommended config for serverless GPU

## Running Tests

Simply run pytest to run the unit & integration tests.

```bash

pytest

```
