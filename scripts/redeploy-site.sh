#!/bin/bash

# Use the directory of the current script to set the project directory
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_dir="$script_dir/.."

# Change to the project directory
cd "$project_dir" || { echo "Failed to cd into project directory"; exit 1; }

# Run the command to make sure the repo inside VPS has the latest changes
git fetch && git reset origin/main --hard || { echo "Failed to update repository"; exit 1; }

# Spin containers down to prevent out of memory issues on VPS instances when building
docker compose -f docker-compose.prod.yml down || { echo "Failed to spin containers down"; exit 1; }

# Build and run the containers
docker compose -f docker-compose.prod.yml up -d --build || { echo "Failed to build and run containers"; exit 1; }

# Check that the Docker containers are running
containers_status=$(docker ps -q)
if [ -n "$containers_status" ]; then
  echo "Deployment Successful, containers are running"
else
  echo "Containers are not running"
fi
