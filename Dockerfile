FROM nvidia/cuda:12.0.0-base-ubuntu22.04

RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

# Default port for documentation, actual port set by environment variable
EXPOSE 8080

# Use shell form to ensure environment variable expansion
CMD uvicorn src.main:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 75