set -e

# Go to the directory of this script
cd "$(dirname "$0")"

src_dir=$(pwd)

# Go to the root directory of the project
cd ../../..

# Go to dataset directory
cd dataset

# iterate over all the folders
for folder in */; do
    # Go to the folder
    cd $folder

    # if it doesn't contain a csv file, skip it
    ls *.csv || continue

    # Get the csv file
    csv_file=$(ls *.csv)

    # get audio folder name
    audios_dir=$(ls -d */)

    # Run the Python script
    python $src_dir/data.py \
        --csv_path "$csv_file" \
        --audios_dir "$audios_dir" \
        --manifest_path "./manifest.tsv" \
        --transcription_path "./transcription.txt"

    # Run tokenizer script
    python $src_dir/tokenizer.py \
        --corpus_path "./transcription.txt" \
        --output_text_path "./processed_text.txt" \
        --model_prefix "tokenizer"

    # Run fairseq-preprocess
    fairseq-preprocess --only-source --trainpref="./processed_text.txt" --destdir="./bin_data" --workers=4

    # Go back to the dataset directory
    cd ..
done
