#!/bin/bash
set -e

# change working directory to the scripts directory
cd "$(dirname "$0 ")"

# go to embedding directory
cd ../embedding

# install requirements
pip install -r requirements.txt
