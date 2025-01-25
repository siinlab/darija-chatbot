set -e

# Go to the directory of this script
cd "$(dirname "$0")"

src_dir=$(pwd)
model_path="$src_dir/checkpoints/"
audios_dir="$src_dir/../../../dataset/amina-2/audios"

python $src_dir/predict.py --model $model_path \
   --audios $audios_dir/0.mp3 $audios_dir/1.mp3 $audios_dir/2.mp3
