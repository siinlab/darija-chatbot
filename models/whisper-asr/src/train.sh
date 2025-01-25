set -e

# Go to the directory of this script
cd "$(dirname "$0")"

src_dir=$(pwd)
hf_dataset_path="$src_dir/../../../dataset/all-datasets-hf"
checkpoints_dir="$src_dir/../checkpoints"

python "$src_dir/train.py" \
   --data-dir "$hf_dataset_path" \
   --output-dir "$checkpoints_dir" \
   --per_device_train_batch_size 16 \
   --per_device_eval_batch_size 8 \
   --learning_rate 5e-5 \
   --warmup_steps 500 \
   --max_steps 5000 --save_steps 250 --eval_steps 250 \
   --generation_max_length 512 \
   --fp16
