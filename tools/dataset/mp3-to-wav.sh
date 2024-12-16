#!/bin/bash
set -e

# accept dataset directory as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <dataset-directory>"
    exit 1
fi

dataset_dir=$(realpath $1)
cd $dataset_dir

# Get the csv file
csv_file="$dataset_dir/data.csv"

# get audio folder name
audios_dir="$dataset_dir/audios"

######################## convert mp3 to wav ########################

# Convert audio files from mp3 to wav
cd "$audios_dir"
echo "Converting mp3 files to wav"

# Count total mp3 files
total_files=$(ls *.mp3 2>/dev/null | wc -l)
if [ "$total_files" -eq 0 ]; then
    echo "No mp3 files found in $audios_dir"
    exit 0
fi

processed_files=0

for file in *.mp3; do
    output="${file%.mp3}.wav"
    # convert mp3 to wav and mono to stereo and to 16kHz
    if [ ! -f "$output" ]; then
        ffmpeg -hide_banner -loglevel error -i "$file" -ar 16000 -ac 1 "$output"
    else
        echo "Skipping $output (already exists)"
    fi
    processed_files=$((processed_files + 1))
    
    # Calculate progress
    progress=$((processed_files * 100 / total_files))
    printf "\rProgress: [%-50s] %d%%" $(printf '#%.0s' $(seq 1 $((progress / 2)))) $progress
done

echo -e "\nConversion complete."

# Remove mp3 files
rm *.mp3 || true
echo "Deleted mp3 files"
cd ..

# In csv file, replace mp3 with wav
echo "Updating csv file"
sed -i 's/\.mp3/\.wav/g' $csv_file
