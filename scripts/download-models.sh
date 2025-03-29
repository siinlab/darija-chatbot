#!/bin/bash
set -e

# Go to the directory of this script
cd "$(dirname "$0")"

# Go to the models folder
cd ../models

# find all .dvc files in the models directory
dvc_files=$(find . -type f -name "*.dvc")

# Pull the artifacts from the storage
for dvc_file in $dvc_files; do
    dvc pull "$dvc_file"
done