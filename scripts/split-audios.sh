#!/bin/bash
set -e

# read audios folder from the user
audios_dir=$(realpath "$1")
output_dir=$(realpath "$2")

# Go to the directory of this script
cd "$(dirname "$0")"
cd ..

script_dir="$(pwd)/data/audio_splitting"

# Iterate over all the audio files in the audios directory
for audio_file in "$audios_dir"/*.mp3; do
    echo "========== Processing: $audio_file =========="
    # Get the filename without the extension
    filename=$(basename -- "$audio_file")
    filename="${filename%.*}"

    # Split the audio file into 5-second chunks
    python "$script_dir/whisper_based.py" "$audio_file" "$output_dir/$filename" --min_silence_duration 200
done
