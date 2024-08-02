#!/bin/bash
set -e

# Change directory to the root of the repository
cd "$(dirname "$0")"
cd ..

# Copy the pre-commit hook to the .git/hooks directory
cp .git-hooks/pre-commit.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit