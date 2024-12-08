set -e

# Go to the directory of this script
cd "$(dirname "$0")"

src_dir=$(pwd)
repo_dir="$src_dir/../tts-arabic-pytorch"
datasets_dir="$src_dir/../../../dataset"
all_datasets_dir="$src_dir/../../../dataset/all-datasets"
tools_dir="$src_dir/../../../tools/dataset"

# Delete all-datasets directory if exists
if [ -d "$all_datasets_dir" ]; then
    rm -r "$all_datasets_dir"
fi

# Get all folders in datasets_dir
folders=$(ls $datasets_dir/*/ -d)

# list folders in one line
folders=$(echo $folders | tr '\n' ' ')
echo "Folders: $folders"
exit 2

# Merge datasets in all-datasets directory
python $tools_dir/merge-datasets.py --datasets "$folders" --output "$all_datasets_dir"

exit 1

# Extract pitch from audio files
cd "$repo_dir"
cp "$src_dir/extract_f0_penn.py" .
output=$(python extract_f0_penn.py --audios_dir "$datasets_dir/audios")

mean=$(echo "$output" | grep -oP "mean \K[0-9.]+")
std=$(echo "$output" | grep -oP "std \K[0-9.]+")

printf "%s\n" $output
echo "Mean: $mean"
echo "Std: $std"

# Generate config file for model training
cd "$src_dir"
python generate-config.py --train_data_path "$datasets_dir" --output_path "config.yaml" \
    --f0_mean "$mean" --f0_std "$std" --restore_model "$repo_dir/pretrained/fastpitch_raw_ms.pth"
