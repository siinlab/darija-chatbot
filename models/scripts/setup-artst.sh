#!/bin/bash
set -e

# change working directory to the scripts directory
cd "$(dirname "$0")"

# go to ArTST folder
cd ../ArTST
current_dir=$(pwd)

# setup ArTST repository
cd "$current_dir/ArTST"
pip install -r requirements.txt

# setup fairseq repository
cd "$current_dir/fairseq"
pip install --editable ./
python setup.py build_ext --inplace
