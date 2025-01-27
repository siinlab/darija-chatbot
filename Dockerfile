FROM ubuntu:22.04
LABEL org.opencontainers.image.source="https://github.com/siinlab/darija-tts"

ENV DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-c"]

WORKDIR /app

# Copy the source code
COPY . .

# Setup environment
RUN bash scripts/setup.sh && bash scripts/install-pyenv.sh && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up pyenv in the shell
ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PYENV_ROOT/versions:$PATH"
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc && \
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# Install dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt && pip install --no-cache-dir -r requirements.txt

# Set up the DVC remote
ARG CDN_API_KEY

# Pull files from the CDN
RUN dvc remote modify --local bunny password $CDN_API_KEY && dvc pull dataset/*.dvc

# Overwrite CDN API key
RUN dvc remote modify --local bunny password 'tmp'

