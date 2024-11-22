#!/bin/bash
set -e

# change working directory to the scripts directory
cd "$(dirname "$0")"

# go to ArTST folder
cd ../ArTST
current_dir=$(pwd)

# pull submodules
git submodule update --init --recursive

# setup ArTST repository
cd "$current_dir/ArTST"
pip install -r requirements.txt

# setup fairseq repository
cd "$current_dir/fairseq"
# Force torch version to 2.1.0 to avoid spending time resolving dependencies
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 lgg
pip install --editable ./
python setup.py build_ext --inplace

# Setup speechbrain
pip install git+https://github.com/speechbrain/speechbrain.git@develop

