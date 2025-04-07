#!/bin/bash
set -e

N_PARALLEL=2

# Read audios folder from the user
audios_dir=$(realpath "$1")
output_dir=$(realpath "$2")

# Go to the directory of this script
cd "$(dirname "$0")"
cd ..

script_dir="$(pwd)/data/audio_splitting"

# Ensure GNU Parallel is installed
if ! command -v parallel &> /dev/null; then
    echo "Error: GNU Parallel is not installed. Install it using: sudo apt-get install parallel"
    exit 1
fi

# Run parallel processing
find "$audios_dir" -maxdepth 1 -type f -name "*.mp3" | parallel --line-buffer -j $N_PARALLEL python "$script_dir/whisper_based.py" {} "$output_dir/{/.}" --min_silence_duration 200

echo "✅ All audio files processed in parallel!"
