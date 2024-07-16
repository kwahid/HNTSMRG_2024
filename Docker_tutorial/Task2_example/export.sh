#!/usr/bin/env bash

# Stop at first error
set -e

./build.sh

DOCKER_TAG="example-algorithm-task-2-mid-rt-segmentation" # change this as needed

echo "=+= Exporting the Docker image to a tar.gz file"
docker save $DOCKER_TAG | gzip -c > ${DOCKER_TAG}.tar.gz

echo "=+= Docker image exported successfully to ${DOCKER_TAG}.tar.gz"