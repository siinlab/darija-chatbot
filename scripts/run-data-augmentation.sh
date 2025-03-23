#!/bin/bash
set -e

# read one argument from the user: datasets folder
if [ "$#" -ne 1 ]; then
    echo "Usage: bash $0 <datasets-folder>"
    exit 1
fi

# check if the datasets folder exists
if [ ! -d "$1" ]; then
    echo "Error: Datasets folder does not exist."
    exit 1
fi

datasets_dir=$(realpath "$1")

# change working directory to the project root directory
cd "$(dirname "$0")/.."
root_dir=$(pwd)
concat_all_audios_dataset_dir="$datasets_dir/concat_all_audios"
spedup_audios_dataset_dir="$datasets_dir/spedup_audios"

concat_yt_audios_dataset_dir="$datasets_dir/concat_yt_audios"
yt_audios_dataset_dir="$datasets_dir/random-2"

# change working directory to the data/ directory
cd "$root_dir/data/augment"

# Speed up audio files
python speedup_audio.py "$datasets_dir" "$spedup_audios_dataset_dir" \
    --min_speed 1.1 \
    --max_speed 1.5 \
    --num_augmented_samples 5000

# Concat audio files
python concat_audios.py "$datasets_dir" "$concat_all_audios_dataset_dir" \
    --max_num_audios_to_merge 4 \
    --silence_duration 100 \
    --num_augmented_samples 10000

# Concat audio files from YouTube
python concat_audios.py "$yt_audios_dataset_dir" "$concat_yt_audios_dataset_dir" \
    --max_num_audios_to_merge 4 \
    --silence_duration 100 \
    --num_augmented_samples 10000