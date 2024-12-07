#!/bin/bash
set -e

# change working directory to the scripts directory
cd "$(dirname "$0 ")"

# Goto the TTS folder
cd ../tts-arabic-pytorch/

# pull submodules
git submodule update --init --recursive

# copy 
cp ./src/download_files.py ./tts-arabic-pytorch/

# download model files
python download_files.py