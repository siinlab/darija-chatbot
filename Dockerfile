FROM ubuntu:22.04
LABEL org.opencontainers.image.source="https://github.com/siinlab/darija-tts"

ENV DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-c"]

# Set the working directory
WORKDIR /app

# Copy the source code
COPY ./scripts ./scripts

# Setup environment and pyenv in a single layer
RUN bash scripts/setup.sh && \
    bash scripts/install-pyenv.sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    echo 'export PYENV_ROOT="/root/.pyenv"' >> ~/.bashrc && \
    echo 'export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PYENV_ROOT/versions:$PATH"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc && \
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PYENV_ROOT/versions:$PATH"
    
# Install Python dependencies
COPY ./requirements*.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt -r requirements.txt

# Copy the DVC files
COPY ./.dvc ./.dvc
COPY ./dataset ./dataset
COPY ./models/tts/checkpoints-female.dvc ./models/tts/checkpoints-female.dvc
COPY ./models/tts/checkpoints-male.dvc ./models/tts/checkpoints-male.dvc
COPY ./models/whisper_asr/checkpoints.dvc ./models/whisper_asr/checkpoints.dvc

# Pull files from the CDN
RUN --mount=type=secret,id=CDN_API_KEY \
    git init && \
    dvc remote modify --local bunny password "$(cat /run/secrets/CDN_API_KEY)" && \
    dvc pull && \
    dvc remote remove --local bunny && \
    rm -rf .dvc/cache && \
    rm -rf .git

# Copy the rest of the source code
COPY . .
