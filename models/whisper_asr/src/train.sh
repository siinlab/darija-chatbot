#!/bin/bash
set -e

# Go to the directory of this script
cd "$(dirname "$0")"

src_dir=$(pwd)
hf_dataset_path="$src_dir/../../../datasets/whisper-all-datasets-hf/"
checkpoints_dir="$src_dir/../checkpoints"

# export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

python "$src_dir/train.py" \
   --data-dir "$hf_dataset_path" \
   --output-dir "$checkpoints_dir" \
   --per_device_train_batch_size 16 \
   --per_device_eval_batch_size 8 \
   --learning_rate 1e-5 \
   --warmup_steps 500 \
   --max_steps 17500 --save_steps 1000 --eval_steps 1000 \
   --generation_max_length 512 \
   --fp16
