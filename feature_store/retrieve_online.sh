curl -X POST \
-H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
-H "Content-Type: application/json; charset=utf-8" \
-d @request1.json \
"https://asia-southeast1-aiplatform.googleapis.com/v1/projects/mitochondrion-project-344303/locations/asia-southeast1/featurestores/marketing_featurestore/entityTypes/users:readFeatureValues"

