#!/bin/bash
set -e

# change working directory to the project root directory
cd "$(dirname "$0")/.."
root_dir=$(pwd)
datasets_dir="$root_dir/dataset"
concat_audios_dataset_dir="$datasets_dir/concat_audios"
spedup_audios_dataset_dir="$datasets_dir/spedup_audios"

# change working directory to the data/ directory
cd "$root_dir/data/augment"

# Speed up audio files
python speedup_audio.py "$datasets_dir" "$spedup_audios_dataset_dir" \
    --min_speed 1.1 \
    --max_speed 1.5 \
    --num_augmented_samples 1000

# Concat audio files
python concat_audios.py "$datasets_dir" "$concat_audios_dataset_dir" \
    --max_num_audios_to_merge 3 \
    --silence_duration 200 \
    --num_augmented_samples 1000
