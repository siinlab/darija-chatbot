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
