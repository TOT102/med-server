#!/bin/bash

# variables
CONTAINER_NAME=med-service
IMAGE_NAME=med-service
HOST_UPLOADS=/opt/.../uploads
HOST_OUTPUT=/opt/.../output
CONTAINER_UPLOADS=/app/app/uploads
CONTAINER_OUTPUT=/app/app/output

echo "🔵 Starting activation script..."

# Stop and remove existing container if it exists
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "🛑 Stopping and removing existing container: $CONTAINER_NAME"
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# Build Docker image
echo "🐳 Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME .

# Create upload and output directories if they don't exist
echo "📁 Ensuring host directories exist..."
mkdir -p $HOST_UPLOADS
mkdir -p $HOST_OUTPUT

# Run new container with volume bindings
echo "🚀 Running container: $CONTAINER_NAME"
docker run -d \
  --name $CONTAINER_NAME \
  -p 5000:5000 \
  -v $HOST_UPLOADS:$CONTAINER_UPLOADS \
  -v $HOST_OUTPUT:$CONTAINER_OUTPUT \
  $IMAGE_NAME

echo "✅ Container $CONTAINER_NAME is now running and operational!"

#USAGE
#chmod +x activate.sh
#./activate.sh