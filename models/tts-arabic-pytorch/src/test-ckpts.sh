set -e

# Check if the checkpoints directory is provided
ckpts_dir=$(realpath "$1")
ckpts_path=$(ls $ckpts_dir/*.pth)

# ensure that checkpoints directory is not empty
if [ -z "$ckpts_path" ]; then
    echo "Checkpoints directory is empty"
    exit 1
fi

# Go to the directory of this script
cd "$(dirname "$0")"
src_dir=$(pwd)

# copy updated script file
cp "$src_dir/test_raw_model.py" ../tts-arabic-pytorch/

# Go to the directory of the TTS model
cd ../tts-arabic-pytorch/

# delete results folder
rm -rf $src_dir/../results || true

# run script
for ckpt_path in $ckpts_path; do
    ckpt_name=$(basename "$ckpt_path")
    ckpt_name="${ckpt_name%.*}"
    python test_raw_model.py --use_cuda --ckpt_path "$ckpt_path" --out_dir "$src_dir/../results/$ckpt_name"
done
