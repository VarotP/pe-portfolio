#!/bin/bash
#
# Tests the timeline_post POST, GET and DELETE endpoints.
# Creates a random timeline post, verifies it shows up in the GET response,
# then deletes it and verifies it's gone.

set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:5000}"
ENDPOINT="${BASE_URL}/api/timeline_post"

# Generate a random post so repeated runs don't collide.
SUFFIX="$RANDOM"
NAME="Test User ${SUFFIX}"
EMAIL="test${SUFFIX}@example.com"
CONTENT="Random test content ${SUFFIX}"

echo "POST ${ENDPOINT}"
echo "  name=${NAME}"
echo "  email=${EMAIL}"
echo "  content=${CONTENT}"

# Create the post via form-encoded data (matches request.form.get in the app).
POST_RESPONSE=$(curl -s -f -X POST "${ENDPOINT}" \
    --data-urlencode "name=${NAME}" \
    --data-urlencode "email=${EMAIL}" \
    --data-urlencode "content=${CONTENT}")

echo "POST response: ${POST_RESPONSE}"

# Pull the new post's id out of the JSON response (POST returns model_to_dict).
POST_ID=$(echo "${POST_RESPONSE}" | grep -o '"id"[[:space:]]*:[[:space:]]*[0-9]*' | grep -o '[0-9]*$')
if [ -z "${POST_ID}" ]; then
    echo "FAIL: could not parse id from POST response"
    exit 1
fi
echo "Created post id=${POST_ID}"

echo "GET ${ENDPOINT}"
GET_RESPONSE=$(curl -s -f "${ENDPOINT}")

# Verify the unique content we just posted is present in the GET response.
if echo "${GET_RESPONSE}" | grep -q "${CONTENT}"; then
    echo "PASS: created post found in GET response"
else
    echo "FAIL: created post NOT found in GET response"
    echo "GET response was: ${GET_RESPONSE}"
    exit 1
fi

echo "DELETE ${ENDPOINT}/${POST_ID}"
DELETE_RESPONSE=$(curl -s -f -X DELETE "${ENDPOINT}/${POST_ID}")
echo "DELETE response: ${DELETE_RESPONSE}"

# Verify the post is no longer present in the GET response.
GET_AFTER=$(curl -s -f "${ENDPOINT}")
if echo "${GET_AFTER}" | grep -q "${CONTENT}"; then
    echo "FAIL: post still present after DELETE"
    exit 1
else
    echo "PASS: post removed after DELETE"
    exit 0
fi
