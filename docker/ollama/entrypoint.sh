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

# Keep the container running
wait