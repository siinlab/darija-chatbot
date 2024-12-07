set -e

# Go to the directory of this script
cd "$(dirname "$0")"

src_dir=$(pwd)

# copy updated script file
cp "$src_dir/train_fp_adv.py" ../tts-arabic-pytorch/

# Go to the directory of the TTS model
cd ../tts-arabic-pytorch/

# run script
python train_fp_adv.py --config_path "$src_dir/config.yaml"
