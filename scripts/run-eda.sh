#!/bin/bash
set -e

# read two arguments from the user: datasets folder and runs folder
if [ "$#" -ne 2 ]; then
    echo "Usage: bash $0 <datasets-folder> <runs-folder>"
    exit 1
fi

# check if the datasets folder exists
if [ ! -d "$1" ]; then
    echo "Error: Datasets folder does not exist."
    exit 1
fi

datasets_folder=$(realpath "$1")
mkdir -p "$2"
runs_folder=$(realpath "$2")

# change working directory to the project root directory
cd "$(dirname "$0")/.."
root_dir=$(pwd)

# get list of all dataset folders in the dataset/ directory
dataset_folders=$(ls -d "$datasets_folder"/*/)

# sort the dataset folders
dataset_folders=$(echo "$dataset_folders" | tr ' ' '\n' | sort)

# change working directory to the data/ directory
cd "$root_dir/data"

# loop through each dataset folder
for dataset_folder in $dataset_folders; do
    # get the dataset name from the folder name
    dataset_name="$(basename "$dataset_folder")"
    echo ">>>> Running EDA for dataset: $dataset_name"

    # run the EDA script
    python eda/cli.py --data "$dataset_folder" --run-dir "$runs_folder/$dataset_name"
done
