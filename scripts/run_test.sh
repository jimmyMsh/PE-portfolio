#!/bin/bash

# Change to the parent directory of the current script, which is in the scripts folder for the project
cd "$(pwd)/.."

# Run the Python unittest command
./site_env/bin/python -m unittest discover -v tests/
