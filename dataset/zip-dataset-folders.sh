#!/bin/bash
cd "$(dirname "$0")" || exit

# iterate over all folders in the current directory
for dir in */; do
    # zip the folder
    echo zip -r "${dir%/}.zip" "$dir"
    zip -q -r "${dir%/}.zip" "$dir"

    # remove the folder
    # rm -rf "$dir"
done
