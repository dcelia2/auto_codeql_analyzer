#!/usr/bin/env bash

IMAGE_NAME="autocodeqlanalyzer"
CONTAINER_NAME="AutoCodeQLAnalyzer"

# Build si l'image n'existe pas
if ! docker image exists "$IMAGE_NAME"; then
    echo "Image introuvable, build en cours..."
    docker build -t "$IMAGE_NAME" .
fi

# Lancer si le container existe déjà, sinon le créer
if docker container exists "$CONTAINER_NAME"; then
    docker start -ai "$CONTAINER_NAME" 
else
    docker run -it --name "$CONTAINER_NAME" -v ./:/workspace "$IMAGE_NAME"
fi
