#!/bin/bash
set -e

# Go to the directory of this script
cd "$(dirname "$0")"

# Go to the root directory of the project
cd ..

# Pull the artifacts from the storage
dvc pull

# Unpack datasets
cd datasets
bash untar-dataset-archives.sh