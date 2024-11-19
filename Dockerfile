FROM Ubuntu:24.04

WORKDIR /app

# Copy the source code
COPY . .

# Install dependencies
# RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

