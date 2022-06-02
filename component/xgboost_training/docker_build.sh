#!/bin/bash
PROJECT_ID="mitochondrion-project-344303"
REGION="asia-southeast2"
REPOSITORY="mitochondrion-components"
IMAGE="xgboost-training:latest"

docker build --tag=$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE .