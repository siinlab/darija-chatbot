#!/bin/bash
set -e

# This file will be located in .git/hooks/pre-push, 
# so we need to change directory to the root of the repository
cd "$(dirname "$0")"
cd ../../

# Run all linters
./tools/linter/run_shellcheck.sh
./tools/linter/run_ruff.sh