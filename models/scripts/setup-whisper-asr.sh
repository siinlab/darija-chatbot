#!/bin/bash
set -e

# change working directory to the scripts directory
cd "$(dirname "$0 ")"

# Goto the TTS folder
cd ../whisper-asr/

pip install datasets>=2.6.1 librosa evaluate>=0.30 jiwer gradio accelerate==0.20.1 transformers[torch] googletrans==4.0.0-rc1