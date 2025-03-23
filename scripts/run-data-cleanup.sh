#!/bin/bash
set -e

# read one argument from the user: runs folder
if [ "$#" -ne 1 ]; then
    echo "Usage: bash $0 <runs-folder>"
    exit 1
fi

# check if the runs folder exists
if [ ! -d "$1" ]; then
    echo "Error: runs folder does not exist."
    exit 1
fi

runs_directory=$(realpath "$1")

# change working directory to the project root directory
cd "$(dirname "$0")/.."
root_dir=$(pwd)

# change working directory to the data/ directory
cd "$root_dir/data/cleanup"

python cli.py --runs_dir "$runs_directory"
