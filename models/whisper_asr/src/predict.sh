#!/bin/bash
set -e

# Go to the directory of this script
cd "$(dirname "$0")"

src_dir=$(pwd)
model_path="$src_dir/../checkpoints/"
audios_dir="$src_dir/../../../dataset/.test-dataset/audios/"

python "$src_dir/predict.py" \
    --model "$model_path" \
    --audios "$audios_dir" \
    --num-samples 200 \
    --output-dir "$src_dir/../results"
