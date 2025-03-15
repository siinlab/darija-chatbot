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

# check if the runs folder exists
if [ ! -d "$2" ]; then
    echo "Error: Datasets folder does not exist."
    exit 1
fi

datasets_dir=$(realpath "$1")
runs_dir=$(realpath "$2")

# change working directory to the project root directory
cd "$(dirname "$0")/.."
root_dir=$(pwd)

# change working directory to the data/ directory
cd "$root_dir/data/filter"

python cli.py --runs_dir "$runs_dir"

# copy filtered.csv files to data/*/ directories
for dataset_folder in "$runs_dir"/*/; do
    dataset_name="$(basename "$dataset_folder")"
    cp "$runs_dir/$dataset_name/filtered.csv" "$datasets_dir/$dataset_name/data.csv"
done
