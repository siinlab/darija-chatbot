#!/bin/bash
cd "$(dirname "$0")" || exit

# iterate over all tar.gz files in the current directory and untar them
for file in *.tar.gz; do
    # untar the file
    echo tar --checkpoint=2000 --checkpoint-action=echo="%T" -xzf "$file"
    tar --checkpoint=2000 --checkpoint-action=echo="%T" -xzf "$file"

    # remove the zip file
    rm "$file"
done
