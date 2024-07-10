#!/bin/bash

# Kill all existing tmux sessions
tmux kill-server

# Enter the project directory (use absolute path)
cd ~/pe-portfolio-site || { echo "Failed to cd into pe-portfolio-site"; exit 1; }

# Run the command to make sure the repo inside VPS has the latest changes
git fetch && git reset origin/main --hard

# Activate the venv and install dependencies
source site_env/bin/activate
pip install -r requirements.txt

# Start new detached tmux session with the command to start the server detached
tmux new -s website_instance -d "cd ~/pe-portfolio-site && source site_env/bin/activate && flask run --host=0.0.0.0"

# Print a message indicating the server has started
echo "Flask server started in tmux session 'website_instance'."

