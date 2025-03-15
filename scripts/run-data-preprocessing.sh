#!/bin/bash
set -e

# change working directory to the project root directory
cd "$(dirname "$0")"

scripts_dir=$(pwd)

cd ..

# check if dataset/ directory exists
if [ -d "dataset/" ]; then
    echo "dataset/ directory already exists. Please remove it before running this script."
    exit 1
fi

# ensure that raw-dataset/ directory exists
if [ ! -d "raw-dataset/" ]; then
    echo "raw-dataset/ directory does not exist. Please create it and add the raw dataset files before running this script."
    exit 1
fi

# ensure raw-dataset contains many directories
if [ ! "$(ls -A raw-dataset/*/)" ]; then
    echo "raw-dataset/ directory is empty. Please add the raw dataset folders before running this script."
    exit 1
fi

# copy raw dataset to dataset/ directory
echo "Copying raw dataset to dataset/ directory..."
cp -r raw-dataset/ dataset/

cd "$scripts_dir"

# run EDA
echo "Running EDA..."
bash run-eda.sh

# run data filtering
echo "Running data filtering..."
bash run-data-filter.sh

# run data augmentation
echo "Running data augmentation..."
bash run-data-augmentation.sh

# run EDA again
echo "Running EDA again..."
bash run-eda.sh

# run data filtering again
echo "Running data filtering again..."
bash run-data-filter.sh
