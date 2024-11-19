#!/bin/bash
set -e

# change working directory to the scripts directory
cd "$(dirname "$0")"

# Install dependencies
apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

# install pyenv
curl https://pyenv.run | bash

# add pyenv to the shell configuration file
# shellcheck disable=SC2016
{
  echo 'export PYENV_ROOT="$HOME/.pyenv"'
  echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"'
  echo 'eval "$(pyenv init -)"'
  echo 'eval "$(pyenv virtualenv-init -)"'
} >> ~/.bashrc

# Install Python 3.8.20
pyenv install 3.8.20

# Install Python 3.10.15
pyenv install 3.10.15