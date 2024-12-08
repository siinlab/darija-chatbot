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
for file in *; do
    # ignore non mp3 files
    if [ "${file##*.}" != "mp3" ]; then
        continue
    fi
    output="${file%.mp3}.wav"
    # convert mp3 to wav and mono to stereo and to 16kHz
    if [ ! -f "$output" ]; then
        ffmpeg -hide_banner -loglevel error -i "$file" -ar 16000 -ac 1 "$output"
    else
        echo "Skipping $output (already exists)"
        continue
    fi
done

# Remove mp3 files
rm *.mp3 || true
echo "Deleted mp3 files"
cd ..

# In csv file, replace mp3 with wav
echo "Updating csv file"
sed -i 's/\.mp3/\.wav/g' $csv_file
