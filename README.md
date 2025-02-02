# DeepSeek Inference API

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

```
