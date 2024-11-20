FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Copy the source code
COPY . .

# Setup environment
RUN bash scripts/install-pyenv.sh

SHELL ["/bin/bash", "-c"]

# Test Pyenv
RUN $HOME/.pyenv/bin/pyenv --version

# Install dependencies
RUN source pip install -r requirements-dev.txt
RUN pip install -r requirements.txt


