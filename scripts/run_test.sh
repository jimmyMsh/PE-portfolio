#!/bin/bash

# Use the directory of the current script to set the project directory
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_dir="$script_dir/.."

# Change to the project directory
cd "$project_dir" || { echo "Failed to cd into project directory"; exit 1; }

# Run the Python unittest command
./site_env/bin/python -m unittest discover -v tests/
