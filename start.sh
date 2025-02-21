#!/bin/bash

# Check if melange is installed
if ! command -v melange &> /dev/null; then
    echo "Installing melange CLI..."
    curl -LO https://github.com/chainguard-dev/melange/releases/latest/download/melange-linux-amd64
    chmod +x melange-linux-amd64
    sudo mv melange-linux-amd64 /usr/local/bin/melange
fi

# Create data directory for ChromaDB if it doesn't exist
mkdir -p data/chromadb

# Start the services using melange
echo "Starting AI Orchestration System..."
melange up

# Show logs
echo "Services are running. Showing logs..."
melange logs -f

# Cleanup on script interrupt
trap 'melange down' INT TERM
