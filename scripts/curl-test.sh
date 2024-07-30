#!/bin/bash

# This script performs end-to-end tests to ensure the entire stack, including 
# NGINX, Docker, and the application, works together as intended, apart from the unit tests I have implemented.

# Set the base URL to test endpoints
BASE_URL="https://jimmymishan.duckdns.org/api/timeline_post"

# Create a random var to use to make new random user
RANDOM_USER_NUM=$(($RANDOM % 100))

# Create the test user information
NAME="testuser${RANDOM_USER_NUM}"
EMAIL="${NAME}.case@google.com"
CONTENT="This is test content created at $(date)"

# Using all of the user information, create a timeline post with a POST operation
POST_TEMP=$(mktemp)
curl -s -o "$POST_TEMP" -X POST "${BASE_URL}" -d "name=${NAME}&email=${EMAIL}&content=${CONTENT}"
POST_RESPONSE=$(cat "$POST_TEMP")
rm "$POST_TEMP"

# Save the ID of this result to delete this post later in raw string (to get rid of quotes)
ID=$(echo $POST_RESPONSE | jq '.id')

# Get all of the data on the DB so far using GET
GET_TEMP=$(mktemp)
curl -s -o "$GET_TEMP" -X GET "${BASE_URL}"
GET_RESPONSE=$(cat "$GET_TEMP")
rm "$GET_TEMP"

# Check if the post we created was added using grep (\ is escape)
if echo "$GET_RESPONSE" | grep -q "\"id\":${ID}"; then
  echo "Success: The new post was found in the GET response and will be deleted."
  # Also delete this post
  DELETE_TEMP=$(mktemp)
  curl -s -o "$DELETE_TEMP" -X DELETE "${BASE_URL}/${ID}"
  rm "$DELETE_TEMP"
else
  echo "Error: The new post was not found in the GET response."
fi

