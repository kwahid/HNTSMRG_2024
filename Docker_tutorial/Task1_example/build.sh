#!/usr/bin/env bash

# Stop at first error
set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DOCKER_TAG="example-algorithm-task-1-pre-rt-segmentation" # change this as needed

echo "=+= Cleaning up any previous builds"
# Remove any existing Docker images with the same tag
if docker images | grep -q "$DOCKER_TAG"; then
  docker rmi "$DOCKER_TAG" --force
fi

echo "=+= Building the Docker image"
docker build "$SCRIPT_DIR" \
  --platform=linux/amd64 \
  --tag $DOCKER_TAG

echo "=+= Docker image $DOCKER_TAG built successfully"