#!/bin/bash
set -e

# change working directory to the scripts directory
cd "$(dirname "$0 ")"

# Goto the TTS folder
cd ../tts-arabic-pytorch/

# pull submodules
git submodule update --init --recursive

# go to repo
cd tts-arabic-pytorch

# download models
python download_files.py
