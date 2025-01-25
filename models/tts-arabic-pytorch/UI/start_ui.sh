#!/bin/bash
set -e

cd "$(dirname "$0")"

UI_DIR=$(pwd)

# Start the streamlit app
cd "$UI_DIR"
streamlit run Home.py --server.port 8002
