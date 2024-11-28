#!/bin/bash
set -e

# change working directory to the scripts directory
cd "$(dirname "$0 ")"

# go to ArTST folder
cd ../ArTST
current_dir=$(pwd)

# ensure python version is 3.8.20
version=$(python --version 2>&1 | awk '{print $2}')
if [ "$version" != "3.8.20" ]; then
    echo "Please use python 3.8.20. Use" pyenv shell 3.8.20" to switch to the correct version."
    exit 1
fi

# pull submodules
git submodule update --init --recursive

# setup ArTST repository
cd "$current_dir/ArTST"
pip install -r requirements.txt

# setup fairseq repository
cd "$current_dir/fairseq"
# Force torch version to 2.1.0 to avoid spending time resolving dependencies
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0
pip install --editable ./
python setup.py build_ext --inplace

# Setup speechbrain
pip install git+https://github.com/speechbrain/speechbrain.git@develop

# install other deps
pip install lgg soundfile npy-append-array tensorboardX
 
# download HUBERT checkpoint inside fairseq
wget https://dl.fbaipublicfiles.com/hubert/hubert_base_ls960.pt -P "$current_dir/fairseq/examples/hubert/simple_kmeans"
