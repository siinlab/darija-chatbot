set -e

# Go to the directory of this script
cd "$(dirname "$0")"

src_dir=$(pwd)
datasets_dir="$src_dir/../../../dataset"
all_datasets_dir="$src_dir/../../../dataset/all-datasets"
tools_dir="$src_dir/../../../tools/dataset"
hf_dataset_path="$src_dir/../../../dataset/all-datasets.arrow"

# Delete all-datasets directory if exists
if [ -d "$all_datasets_dir" ]; then
    rm -r "$all_datasets_dir"
fi

# Get all folders in datasets_dir
folders=$(ls $datasets_dir/*/ -d)

# list folders in one line
folders=$(echo $folders | tr '\n' ' ')

# Merge datasets in all-datasets directory
python $tools_dir/merge-datasets.py --datasets $folders --output "$all_datasets_dir"

# Convert mp3 files to wav
bash $tools_dir/mp3-to-wav.sh "$all_datasets_dir"

# Build HF dataset
python $src_dir/build-dataset.py --data-dir $all_datasets_dir --output-path $hf_dataset_path
