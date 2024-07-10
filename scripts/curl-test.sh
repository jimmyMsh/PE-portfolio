#!/bin/bash

# Set the base URL to test endpoints
BASE_URL="http://localhost:5000/api/timeline_post"

# Create a random var to use to make new random user
RANDOM_USER_NUM=$(($RANDOM % 100))

# Create the test user information
NAME="testuser${RANDOM_USER_NUM}"
EMAIL="${NAME}.case@google.com"
CONTENT="This is test content created at $(date)"

# Using all of the user information, create a timeline post with a POST operation
POST_RESULT=$(curl -s -X POST "${BASE_URL}" -d "name=${NAME}&email=${EMAIL}&content=${CONTENT}")

# Save the ID of this result to delete this post later in raw string (to get rid of quotes)
ID=$(echo $POST_RESULT | jq '.id')

# Get all of the data on the DB so far using GETG
GET_RESULT=$(curl -s -X GET "${BASE_URL}")

# Check if the post we created was added using grep (\ is escape)
if echo "$GET_RESULT" | grep -q "\"id\":${ID}"; then
  echo "Success: The new post was found in the GET response and will be deleted."
  # Also delete this post
  curl -X DELETE "${BASE_URL}/${ID}"
else
  echo "Error: The new post was not found in the GET response."
fi