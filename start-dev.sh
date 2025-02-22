#!/bin/bash

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
mkdir -p data/chromadb

# Stop any running containers and clean up
echo "Cleaning up existing containers..."
podman stop $(podman ps -aq) 2>/dev/null || true
podman rm $(podman ps -aq) 2>/dev/null || true
podman volume rm redis_data node_modules 2>/dev/null || true
podman network rm ai_network 2>/dev/null || true

# Create network and volumes
echo "Creating network and volumes..."
podman network create ai_network
podman volume create redis_data
podman volume create node_modules

# Build and start services
echo "Building and starting services..."
podman-compose build --pull
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
    echo "User:"
    podman inspect $container --format '{{.Config.User}}'
    echo "Read Only:"
    podman inspect $container --format '{{.HostConfig.ReadonlyRootfs}}'
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
