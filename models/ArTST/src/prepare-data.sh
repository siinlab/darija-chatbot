set -e

# Go to the directory of this script
cd "$(dirname "$0")"

src_dir=$(pwd)

# Go to the root directory of the project
cd ../../..

# Go to dataset directory
cd dataset

# Merge all datasets into one
dataset_folders=$(ls -d */)
python $src_dir/merge-datasets.py --datasets ./wamid ./mohamed-1 ./mohamed-2 --output all-datasets

# Go to all-datasets directory
cd all-datasets

# Remove the previous data
rm -rf embeddings hubert_features dict.txt || true

# Get the csv file
csv_file=$(ls data*.csv)

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

# Run the Python script to create train and valid csv files
# and create train and valid text files
# and create train and valid (manifest) tsv files
python $src_dir/data.py \
    --csv_path "$csv_file" \
    --audios_dir "$audios_dir" \
    --train_path "./train.csv" \
    --valid_path "./valid.csv" \
    --val_size 0.1

# Run tokenizer script
for split in "train" "valid"; do
    python $src_dir/tokenizer.py \
        --corpus_path "./$split.txt" \
        --output_text_path "./$split-processed.txt" \
        --model_type "char" \
        --model_prefix "tokenizer"
done

# Run fairseq-preprocess
fairseq-preprocess --only-source --trainpref="./train-processed.txt" \
    --validpref="./valid-processed.txt" --destdir="." --workers=8

######################## Prepare audios data ########################

for split in "train" "valid"; do
    # Generate hubert features
    python $src_dir/../fairseq/examples/hubert/simple_kmeans/dump_hubert_feature.py \
        . $split $src_dir/../fairseq/examples/hubert/simple_kmeans/hubert_base_ls960.pt \
        6 1 0 ./hubert_features # 6 is the number of layers

    # Generate speaker embedding
    python $src_dir/speaker-embedding.py --tsv_file "./$split.tsv" --output_dir "./embeddings"
done