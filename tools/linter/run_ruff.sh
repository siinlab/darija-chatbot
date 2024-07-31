#!/bin/bash
set -e

cd "$(dirname "$0")"
cd ../../
ruff check .