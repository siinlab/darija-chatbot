#!/bin/bash
set -e

# change working directory to the project root directory
cd "$(dirname "$0")"

# run EDA
bash run-eda.sh

# run data filtering
bash run-data-filter.sh

# run data augmentation
bash run-data-augmentation.sh

# run EDA again
bash run-eda.sh

# run data filtering again
bash run-data-filter.sh
