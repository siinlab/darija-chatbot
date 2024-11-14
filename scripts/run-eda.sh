#!/bin/bash
set -e

# change working directory to the project root directory
cd "$(dirname "$0")/.."
root_dir=$(pwd)

# get list of all dataset folders in the dataset/ directory
dataset_folders=$(ls -d "$root_dir/dataset"/*/)

# change working directory to the data/ directory
cd "$root_dir/data"

# loop through each dataset folder
for dataset_folder in $dataset_folders
do
    # get the dataset name from the folder name
    dataset_name="$(basename "$dataset_folder")"
    echo ">>>> Running EDA for dataset: $dataset_name"

    # run the EDA script
    python eda/cli.py --data "$dataset_folder" --run-dir "$root_dir/runs/eda/$dataset_name"
done