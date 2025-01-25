#!/bin/bash
set -e

# change working directory to the project root directory
cd "$(dirname "$0")/.."
root_dir=$(pwd)

# get list of all dataset folders in the dataset/ directory
runs_dir="$root_dir/runs/eda/"

# change working directory to the data/ directory
cd "$root_dir/data/filter"

python cli.py --runs_dir "$runs_dir"

# copy filtered.csv files to data/*/ directories
for dataset_folder in "$runs_dir"/*/
do
    dataset_name="$(basename "$dataset_folder")"
    cp "$runs_dir/$dataset_name/filtered.csv" "$root_dir/dataset/$dataset_name/data.csv"
done
