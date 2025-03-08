#!/bin/bash
set -e

# Go to the directory of this script
cd "$(dirname "$0")"

src_dir=$(pwd)
model_path="$src_dir/../checkpoints/"
audios_dir="$src_dir/../../../dataset/.test-dataset/audios/bMHW0Zioydg"

python "$src_dir/predict.py" --model "$model_path" --audios "$audios_dir"
