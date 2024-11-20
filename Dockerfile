FROM ubuntu:22.04

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Copy the source code
COPY . .

# Setup environment
RUN bash scripts/install-pyenv.sh

# Set up pyenv in the shell
ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PYENV_ROOT/versions:$PATH"
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc && \
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# Test Pyenv
RUN pyenv --version

# Install dependencies
RUN pip install dvc #-r requirements-dev.txt
# RUN pip install -r requirements.txt

ARG CDN_API_KEY

# Pull files from the CDN
RUN dvc remote modify --local bunny password $CDN_API_KEY && dvc pull