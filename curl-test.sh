#!/bin/bash

API_URL="http://localhost:5000/api/timeline_post"


RANDOM_NAME="User$RANDOM"
RANDOM_EMAIL="user$RANDOM@example.com"
RANDOM_CONTENT="This is a random post content #$RANDOM"


POST_RESPONSE=$(curl -s -X POST $API_URL -d "name=$RANDOM_NAME" -d "email=$RANDOM_EMAIL" -d "content=$RANDOM_CONTENT")

echo "Post response:"
echo "$POST_RESPONSE"

echo "-------------------------------------------------------------------"


# Extract the ID of the last created timeline post from POST_RESPONSE 
POST_ID=$(grep -o '"id":[0-9]*' <<< "$POST_RESPONSE" | grep -o '[0-9]*')



if [ -n "$POST_ID" ]; then
    echo "Created timeline post with ID: $POST_ID"


    echo "Getting all timeline posts..."
    GET_RESPONSE=$(curl -s $API_URL)
    echo "Get response:"
    echo "$GET_RESPONSE"

    echo "---------------------------------------------------------------------"
    echo "Deleting timeline post with ID: $POST_ID..."
    DELETE_RESPONSE=$(curl -s -X DELETE "$API_URL/$POST_ID")
    echo "Delete response:"
    echo "$DELETE_RESPONSE"
else
    echo "Failed to retrieve timeline post ID for deletion."
fi

# GET_RESPONSE=$(curl -s $API_URL)

# echo "---------------------------------------------------------"
# echo "Get response:"
# echo "$GET_RESPONSE"
# echo "--------------------------------------------------------------------"
