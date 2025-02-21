#!/bin/bash

# Create necessary directories
mkdir -p data/chromadb

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

# Start services
echo "Starting AI Orchestration System..."
docker-compose up -d

# Wait for services to be ready
check_service "Backend API" 8000 || exit 1
check_service "Frontend" 3000 || exit 1

echo "All services are running!"
echo "
Access points:
- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs
- Redis: localhost:6379

To view logs:
docker-compose logs -f

To stop services:
docker-compose down
"

# Show logs
docker-compose logs -f
