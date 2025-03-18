#!/bin/bash
set -e

# Ensure the script receives the correct number of arguments
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <checkpoint-directory>"
    exit 1
fi

ckpt_dir=$(realpath "$1")

# Go to the directory of this script
cd "$(dirname "$0")"

# read checkpoint directory
# get parent of ckpt_dir
ckpts_dir=$(dirname "$ckpt_dir")
# copy contents of ckpt_dir to ckpts_dir
cp "$ckpt_dir"/* "$ckpts_dir" || true

src_dir=$(pwd)
audios_dir="$src_dir/../../../datasets/test-dataset/audios/"

python "$src_dir/predict.py" \
    --model "$ckpts_dir" \
    --audios "$audios_dir" \
    --num-samples 500 \
    --output-dir "$src_dir/../prediction-results/"
