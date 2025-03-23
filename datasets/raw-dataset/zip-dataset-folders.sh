#!/bin/bash
cd "$(dirname "$0")" || exit

# iterate over all folders in the current directory
for dir in */; do
    # if the zip file already exists, skip this folder
    if [[ -f "${dir%/}.zip" ]]; then
        echo "Skipping $dir. Zip file already exists."
        continue
    fi
    # zip the folder
    echo zip -r "${dir%/}.zip" "$dir"
    zip -q -r "${dir%/}.zip" "$dir"

    # remove the folder
    rm -rf "$dir"
done
