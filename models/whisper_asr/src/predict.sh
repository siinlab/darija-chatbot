#!/bin/bash
set -e

# Go to the directory of this script
cd "$(dirname "$0")"

# read checkpoint directory
ckpt_dir=$1
# get parent of ckpt_dir
ckpts_dir=$(dirname "$ckpt_dir")
# copy contents of ckpt_dir to ckpts_dir
cp "$ckpt_dir"/* "$ckpts_dir"

src_dir=$(pwd)
audios_dir="$src_dir/../../../dataset/.test-dataset/audios/"

python "$src_dir/predict.py" \
    --model "$ckpts_dir" \
    --audios "$audios_dir" \
    --num-samples 10 \
    --output-dir "$src_dir/../prediction-results/"
