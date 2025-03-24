#!/bin/bash
set -e

# Go to the directory of this script
cd "$(dirname "$0")"

src_dir=$(pwd)
datasets_dir="$src_dir/../../../datasets/whisper-dataset"
all_datasets_dir="$src_dir/../../../datasets/whisper-all-datasets"
hf_dataset_path="$src_dir/../../../datasets/whisper-all-datasets-hf"
tools_dir="$src_dir/../../../tools/dataset"

# Delete all-datasets directory if exists
if [ -d "$all_datasets_dir" ]; then
    rm -r "$all_datasets_dir"
fi

# Get all folders in datasets_dir
folders=$(ls "$datasets_dir"/*/ -d)

# list folders in one line
folders=$(echo "$folders" | tr '\n' ' ')

# Merge datasets in all-datasets directory
# shellcheck disable=SC2086
python "$tools_dir/merge-datasets.py" --datasets $folders --output "$all_datasets_dir"

# Build HF dataset
python "$src_dir/build-dataset.py" --data-dir "$all_datasets_dir" --output-path "$hf_dataset_path"
