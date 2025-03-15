#!/bin/bash
set -e

# change working directory to the project root directory
cd "$(dirname "$0")"

scripts_dir=$(pwd)

cd ..

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
