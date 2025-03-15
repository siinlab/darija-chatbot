#!/bin/bash
set -e

# change working directory to the project root directory
cd "$(dirname "$0")"

scripts_dir=$(pwd)

cd ..

# ensure the datasets/raw-dataset/ directory exists and its size is greater than 1GB
if [ ! -d "datasets/raw-dataset" ]; then
    echo "Error: datasets/raw-dataset/ directory does not exist."
    exit 1
fi

# check the size of the datasets/raw-dataset/ directory
raw_dataset_size=$(du -s datasets/raw-dataset | cut -f1)
if [ "$raw_dataset_size" -lt 1000000 ]; then
    echo "Error: datasets/raw-dataset/ directory is empty or too small."
    exit 1
fi
whisper_dataset_dir=$(realpath "./datasets/whisper-dataset")
rm -rf "$whisper_dataset_dir" ./runs/whisper-data 2>/dev/null || true
mkdir -p "./runs/whisper-data"
runs_dir=$(realpath "./runs/whisper-data")

# copy datasets/raw-dataset/ to datasets/whisper-dataset/
cp -r datasets/raw-dataset "$whisper_dataset_dir"

cd "$scripts_dir"

# run EDA
echo "Running EDA..."
bash run-eda.sh "$whisper_dataset_dir" "$runs_dir"

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
