#!/bin/bash
set -e

# Run the uvicorn command to start the FastAPI application
exec uvicorn src.main:app --host 0.0.0.0 --port 8080
