#!/usr/bin

ENDPOINT_ID="7289542189829324800"
PROJECT_ID="mitochondrion-project-344303"
INPUT_DATA_FILE="INPUT-JSON"

curl \
-X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
https://us-central1-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/us-central1/endpoints/${ENDPOINT_ID}:predict \
-d "@${INPUT_DATA_FILE}"

