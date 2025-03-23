#!/bin/bash
set -e

# change working directory to the project root directory
cd "$(dirname "$0")"

scripts_dir=$(pwd)

cd ..
root_dir=$(pwd)

raw_datasets="$root_dir/datasets/raw-dataset"
whisper_dataset_dir="$root_dir/datasets/whisper-dataset"
runs_dir="$root_dir/runs/whisper-data"

# ensure the datasets/raw-dataset/ directory exists and its size is greater than 1GB
if [ ! -d "$raw_datasets" ]; then
    echo "Error: datasets/raw-dataset/ directory does not exist."
    exit 1
fi

# check the size of the datasets/raw-dataset/ directory
raw_dataset_size=$(du -s "$raw_datasets" | cut -f1)
if [ "$raw_dataset_size" -lt 1000000 ]; then
    echo "Error: datasets/raw-dataset/ directory is empty or too small."
    exit 1
fi

# Delete old build files
echo "Deleting $whisper_dataset_dir and $runs_dir"
rm -rf "$whisper_dataset_dir" "$runs_dir" 2>/dev/null || true

# copy datasets/raw-dataset/ to datasets/whisper-dataset/
echo "Copying datasets/raw-dataset/ to datasets/whisper-dataset/"
cp -r datasets/raw-dataset "$whisper_dataset_dir"

# Goto scripts folder
cd "$scripts_dir"

# run EDA
echo "Running EDA..."
bash run-eda.sh "$whisper_dataset_dir" "$runs_dir"

# run data clean up
echo "Running data cleanup..."
bash run-data-cleanup.sh "$runs_dir"

# run data filtering
echo "Running data filtering..."
bash run-data-filter.sh "$whisper_dataset_dir" "$runs_dir"

# run data augmentation
echo "Running data augmentation..."
bash run-data-augmentation.sh "$whisper_dataset_dir"

# run EDA again
echo "Running EDA again..."
bash run-eda.sh "$whisper_dataset_dir" "$runs_dir"

# run data filtering again
echo "Running data filtering again..."
bash run-data-filter.sh "$whisper_dataset_dir" "$runs_dir"
