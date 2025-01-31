#!/bin/bash
set -e

# change working directory to the scripts directory
cd "$(dirname "$0 ")"

# Goto the TTS folder
cd ../tts/

# pull submodules
git submodule update --init --recursive

# copy 
cp ./src/download_files.py ./tts-arabic-pytorch/

# download model files
cd ./tts-arabic-pytorch/
python download_files.py