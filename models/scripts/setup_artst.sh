#!/bin/bash
set -e

# change working directory to the scripts directory
cd "$(dirname "$0")"

# go to ArTST folder
cd ../ArTST
current_dir=$(pwd)

# install git lfs
apt-get install git-lfs
git lfs install

# clone the ArTST repository
git clone https://github.com/mbzuai-nlp/ArTST || true
git clone https://github.com/pytorch/fairseq || true
# git clone https://huggingface.co/MBZUAI/ArTST ArTST-hf

# setup ArTST repository
cd "$current_dir/ArTST"
pip install -r requirements.txt

# setup fairseq repository
cd "$current_dir/fairseq"
pip install --editable ./
python setup.py build_ext --inplace
