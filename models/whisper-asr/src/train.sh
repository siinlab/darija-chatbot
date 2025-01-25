set -e

# Go to the directory of this script
cd "$(dirname "$0")"

src_dir=$(pwd)
hf_dataset_path="$src_dir/../../../dataset/all-datasets.arrow"


python $src_dir/train.py --data-dir $hf_dataset_path \
 --output-dir $src_dir/checkpoints/ \
