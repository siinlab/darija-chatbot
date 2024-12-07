set -e

# Go to the directory of this script
cd "$(dirname "$0")"

src_dir=$(pwd)
repo_dir="$src_dir/../tts-arabic-pytorch"
datasets_dir="$src_dir/../../../dataset/mohamed-1"

# Generate config file for model training
python generate-config.py --train_data_path "$datasets_dir" --output_path "config.yaml"

# Extract pitch from audio files
cd "$repo_dir"
cp "$src_dir/extract_f0_penn.py" .
python extract_f0_penn.py --audios_dir "$audios_dir/audios"