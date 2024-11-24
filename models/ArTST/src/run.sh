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

    echo "Processing: $folder"

    # Remove the previous data
    rm -rf bin_data embeddings hubert_features || true

    # Get the csv file
    csv_file=$(ls *.csv)

    # get audio folder name
    audios_dir=$(ls -d audio*/)

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
        if [ ! -f "$output" ]; then
            ffmpeg -hide_banner -loglevel error -i "$file" -ar 16000 "$output"
        else
            echo "Skipping $output (already exists)"
        fi
    done
    # Remove mp3 files
    rm *.mp3 || true
    echo "Deleted mp3 files"
    cd ..

    # In csv file, replace mp3 with wav
    sed -i 's/\.mp3/\.wav/g' $csv_file

    ######################## Prepare text data ########################

    # TODO: normalize text by removing punctuation, digits, etc.

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
        --model_type "char" \
        --model_prefix "tokenizer"

    # Run fairseq-preprocess
    fairseq-preprocess --only-source --trainpref="./processed_text.txt" --destdir="./bin_data" --workers=8

    # ######################## Prepare audios data ########################

    # # Generate wav2vec manifest
    python $src_dir/../fairseq/examples/wav2vec/wav2vec_manifest.py "$audios_dir" \
        --dest . --ext wav --valid-percent 0.1

    # # Generate hubert features
    python $src_dir/../fairseq/examples/hubert/simple_kmeans/dump_hubert_feature.py \
        . train $src_dir/../fairseq/examples/hubert/simple_kmeans/hubert_base_ls960.pt \
        6 1 0 ./hubert_features

    # Generate speaker embedding
    python $src_dir/speaker-embedding.py --tsv_file "./train.tsv" --output_dir "./embeddings"
    python $src_dir/speaker-embedding.py --tsv_file "./valid.tsv" --output_dir "./embeddings"

    exit 1

    # Go back to the dataset directory
    cd ..
done
