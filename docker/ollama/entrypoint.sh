#!/bin/bash
set -e

# Start Ollama in the background
ollama serve &

# Wait for Ollama to be ready
sleep 5

# Pull the phi3 model
echo "Pulling phi3 model..."
ollama pull phi3

echo "Phi3 model ready!"

echo "Pulling nomic-embed-text model..."
ollama pull nomic-embed-text

echo "nomic-embed-text model!"

# Keep the container running
wait