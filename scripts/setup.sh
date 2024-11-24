#!/bin/bash
set -e

# change working directory to the scripts directory
cd "$(dirname "$0")"

# Install dependencies
apt-get update -y
apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git portaudio19-dev \
    nvtop htop vim git-lfs ffmpeg libsox-dev tree

# Install git-lfs
git lfs install

# unset the extraheader for github.com 
git config --unset-all http.https://github.com/.extraheader
