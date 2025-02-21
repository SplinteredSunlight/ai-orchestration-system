#!/bin/bash

# Function to check if Podman is installed
check_podman() {
    if ! command -v podman &> /dev/null; then
        echo "Podman is not installed. Installing..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install podman
            podman machine init
            podman machine start
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # For Ubuntu/Debian
            sudo apt-get update && sudo apt-get install -y podman
        fi
    fi
}

# Function to check if a service is healthy
check_service() {
    local service=$1
    local port=$2
    local max_attempts=30
    local attempt=1

    echo "Waiting for $service to be ready..."
    while ! curl -s "http://localhost:$port" > /dev/null; do
        if [ $attempt -eq $max_attempts ]; then
            echo "$service failed to start after $max_attempts attempts"
            return 1
        fi
        attempt=$((attempt + 1))
        sleep 1
    done
    echo "$service is ready!"
    return 0
}

# Create necessary directories
mkdir -p ../data/chromadb

# Ensure Podman is installed
check_podman

# Pull latest Chainguard images
echo "Pulling latest Chainguard images..."
podman pull cgr.dev/chainguard/python:latest-dev
podman pull cgr.dev/chainguard/node:latest-dev
podman pull cgr.dev/chainguard/redis:latest

# Verify image signatures
echo "Verifying image signatures..."
podman image verify cgr.dev/chainguard/python:latest-dev
podman image verify cgr.dev/chainguard/node:latest-dev
podman image verify cgr.dev/chainguard/redis:latest

# Start services with Podman Compose
echo "Starting AI Orchestration System..."
podman-compose up -d

# Wait for services to be ready
check_service "Backend API" 8000 || exit 1
check_service "Frontend" 3000 || exit 1

echo "All services are running!"
echo "
Access points:
- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs
- Redis: localhost:6379

Security Status:
"
# Show security info for running containers
for container in $(podman ps --format "{{.Names}}"); do
    echo "Container: $container"
    echo "Security Options:"
    podman inspect $container --format '{{.HostConfig.SecurityOpt}}'
    echo "Capabilities:"
    podman inspect $container --format '{{.HostConfig.CapDrop}}'
    echo "User:"
    podman inspect $container --format '{{.Config.User}}'
    echo "---"
done

echo "
Commands:
- View logs: podman-compose logs -f
- Stop services: podman-compose down
- Check container status: podman ps
"

# Show logs
podman-compose logs -f
