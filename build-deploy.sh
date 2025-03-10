set -x


gcloud builds submit --config cloudbuild.yaml


export LOCATION=northamerica-northeast1
export CONTAINER_URI=gcr.io/neuroware-453218/deepseek-inference-api:gemma2b
export SERVICE_NAME=inference-api-gemma2b


gcloud beta run deploy $SERVICE_NAME \
   --image=$CONTAINER_URI \
   --port=11434 \
   --cpu=8 \
   --memory=32Gi \
   --no-cpu-throttling \
   --max-instances=3 \
   --concurrency=64 \
   --region=$LOCATION \
   --allow-unauthenticated
