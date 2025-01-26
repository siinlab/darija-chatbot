#!/bin/bash
set -e

cd "$(dirname "$0")"

DEPLOY_DIR=$(pwd)
TTS_DIR="$DEPLOY_DIR/../tts-arabic-pytorch"

# Copy API files to the TTS directory
cp "$DEPLOY_DIR"/*.py "$TTS_DIR"
cp "$DEPLOY_DIR"/*.json "$TTS_DIR"

# Start the API
cd "$TTS_DIR"
uvicorn api:app --host 0.0.0.0 --port 8001 --reload
