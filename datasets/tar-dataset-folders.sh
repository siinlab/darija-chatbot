#!/bin/bash
cd "$(dirname "$0")" || exit

# iterate over all folders in the current directory
for dir in */; do
    # ignore the raw-dataset/ directory
    if [ "$dir" = "raw-dataset/" ]; then
        echo "Skipping raw-dataset/ directory..."
        continue
    fi
    # compress the folder
    echo tar --checkpoint=2000 --checkpoint-action=echo="%T" -czf "${dir%/}.tar.gz" "$dir"
    tar --checkpoint=2000 --checkpoint-action=echo="%T" -czf "${dir%/}.tar.gz" "$dir"

    # remove the folder
    rm -rf "$dir"
done
