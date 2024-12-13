set -e

# Go to the directory of this script
cd "$(dirname "$0")"

src_dir=$(pwd)

ckpt_path=$(realpath "$1")

# copy updated script file
cp "$src_dir/test_raw_model.py" ../tts-arabic-pytorch/

# Go to the directory of the TTS model
cd ../tts-arabic-pytorch/

# run script
python test_raw_model.py --ckpt_path "$ckpt_path"