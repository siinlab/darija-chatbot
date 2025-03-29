#!/bin/bash
set -e

# Go to the directory of this script
cd "$(dirname "$0")"

# Go to the datasets folder
cd ../datasets

# find all .dvc files in the datasets directory
dvc_files=$(find . -type f -name "*.dvc")

# Pull the artifacts from the storage
# shellcheck disable=SC2086
dvc pull $dvc_files

# uncompress the downloaded files
bash untar-dataset-archives.sh
bash raw-dataset/unzip-dataset-archives.sh