#!/bin/bash

set -e

# Wait for Redis to be ready
until nc -z ${REDIS_HOST} ${REDIS_PORT}; do
    echo "Waiting for Redis to be ready..."
    sleep 1
done

# Create data directories if they don't exist
mkdir -p /app/data/chromadb

# Apply any pending migrations (if we add a database later)
# python manage.py migrate

# Initialize ChromaDB collections
python -c "
from app.core.rag_manager import rag_manager
print('Initializing RAG collections...')
rag_manager.collections  # This will create collections if they don't exist
print('RAG collections initialized successfully')
"

# Start the application with the provided command
exec "$@"
