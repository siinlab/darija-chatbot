#!/bin/bash
set -e

# change working directory to the scripts directory
cd "$(dirname "$0")"

# install pyenv
curl https://pyenv.run | bash

# add pyenv to the shell configuration file
# shellcheck disable=SC2016
{
  echo 'export PYENV_ROOT="$HOME/.pyenv"'
  echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"'
  echo 'eval "$(pyenv init -)"'
  echo 'eval "$(pyenv virtualenv-init -)"'
} >>~/.bashrc

# Install Python 3.8.20
# "$HOME/.pyenv/bin/pyenv" install 3.8.20

# Install Python 3.10.15
"$HOME/.pyenv/bin/pyenv" install 3.10.15
"$HOME/.pyenv/bin/pyenv" global 3.10.15
