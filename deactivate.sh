#!/bin/bash

# variables
CONTAINER_NAME=med-service

echo "🔴 Starting deactivation script..."

# Stop the container if running
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "🛑 Stopping running container: $CONTAINER_NAME"
    docker stop $CONTAINER_NAME
else
    echo "ℹ️ No running container named $CONTAINER_NAME found."
fi

# Remove the container if exists
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "🧹 Removing container: $CONTAINER_NAME"
    docker rm $CONTAINER_NAME
else
    echo "ℹ️ No container named $CONTAINER_NAME to remove."
fi

echo "✅ Deactivation complete."
