set -e

# Go to the directory of this script
cd "$(dirname "$0")"

src_dir=$(pwd)
hf_dataset_path="$src_dir/../../../dataset/all-datasets.arrow"


python $src_dir/train.py --data-dir $hf_dataset_path \
 --output-dir $src_dir/checkpoints/ \
 --per_device_train_batch_size 16 \
    --per_device_eval_batch_size 8 \
    --learning_rate 1e-4 \
    --warmup_steps 500 \
    --max_steps 10000 \
    --fp16 \
    --generation_max_length 512 \
    
