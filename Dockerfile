FROM ubuntu:24.04

WORKDIR /app

# Copy the source code
COPY . .

# Show the content of the current directory
RUN ls -la

# Install dependencies
RUN pip install -r requirements-dev.txt

