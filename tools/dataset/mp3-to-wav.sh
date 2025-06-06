#!/bin/bash
set -e

# Accept dataset directory as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <dataset-directory>"
    exit 1
fi

dataset_dir=$(realpath "$1")
cd "$dataset_dir"

# Get the csv file
csv_file="$dataset_dir/data.csv"

# Get audio folder name
audios_dir="$dataset_dir/audios"

######################## Convert mp3 to wav ########################

# Convert audio files from mp3 to wav
cd "$audios_dir"
echo "Converting mp3 files to wav"

# Count total mp3 files
total_files=$(find . -maxdepth 1 -type f -name "*.mp3" | wc -l)
if [ "$total_files" -eq 0 ]; then
    echo "No mp3 files found in $audios_dir"
    exit 0
fi

# Function to process a single file
convert_file() {
    file="$1"
    output="${file%.mp3}.wav"
    if [ ! -f "$output" ]; then
        ffmpeg -hide_banner -loglevel error -i "$file" -ar 16000 -ac 1 "$output"
    else
        echo "Skipping $output (already exists)"
    fi
}

export -f convert_file

# Use GNU parallel to process files in parallel
find . -maxdepth 1 -type f -name "*.mp3" | parallel --bar --jobs "$(nproc)" convert_file

echo -e "\nConversion complete."

# Remove mp3 files
find . -maxdepth 1 -type f -name "*.mp3" -print0 | xargs -0 rm -f
echo "Deleted mp3 files"

# Update the CSV file to replace .mp3 with .wav
echo "Updating csv file"
sed -i 's/\.mp3/\.wav/g' "$csv_file"

echo "Process completed successfully."
