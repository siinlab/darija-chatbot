#!/bin/bash
set -e

# Go to the directory of this script
cd "$(dirname "$0")"

# Go to the models folder
cd ../models

# find all .dvc files in the models directory
dvc_files=$(find . -type f -name "*.dvc")

# Pull the artifacts from the storage
# shellcheck disable=SC2086
dvc pull $dvc_files