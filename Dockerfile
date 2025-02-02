FROM nvidia/cuda:12.0.0-base-ubuntu22.04

RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

# Port will be provided by Cloud Run or can be overridden at runtime
EXPOSE 8080

CMD uvicorn src.main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8080}