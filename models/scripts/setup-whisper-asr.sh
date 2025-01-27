#!/bin/bash
set -e

# change working directory to the scripts directory
cd "$(dirname "$0 ")"

# go to whisper_asr directory
cd ../whisper_asr

# install requirements
pip install -r requirements.txt
