#!/bin/bash

# Build and start all services
echo "Starting AI Orchestration System..."
docker-compose up --build -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 5

# Show logs
echo "Services are running. Showing logs..."
docker-compose logs -f

# Cleanup on script interrupt
trap 'docker-compose down' INT TERM
