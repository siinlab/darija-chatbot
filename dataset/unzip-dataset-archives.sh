#!/bin/bash
cd "$(dirname "$0")" || exit

# iterate over all zip files in the current directory and unzip them
for file in *.zip; do
    # unzip the file
    echo unzip -q "$file"
    unzip -q "$file"

    # remove the zip file
    rm "$file"
done
