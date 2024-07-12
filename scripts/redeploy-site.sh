#!/bin/bash

# Enter the project directory (use absolute path)
cd ~/pe-portfolio-site || { echo "Failed to cd into pe-portfolio-site"; exit 1; }

# Run the command to make sure the repo inside VPS has the latest changes
git fetch && git reset origin/main --hard || { echo "Failed to update repository"; exit 1; }

# Activate the venv and install dependencies
source site_env/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }
pip install -r requirements.txt || { echo "Failed to install dependencies"; exit 1; }

# Restart the service that runs the website
sudo systemctl restart myportfolio || { echo "Failed to restart myportfolio service"; exit 1; }

# Check that the service is running
status=$(systemctl is-active myportfolio)
if [ "$status" = "active" ]; then
  echo "Startup Successful, service is running"
else
  echo "Service is not running"
fi

