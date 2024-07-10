#!/bin/bash

API_URL="http://localhost:5000/api/timeline_post"


RANDOM_NAME="User$RANDOM"
RANDOM_EMAIL="user$RANDOM@example.com"
RANDOM_CONTENT="This is a random post content #$RANDOM"


POST_RESPONSE=$(curl -s -X POST $API_URL -d "name=$RANDOM_NAME" -d "email=$RANDOM_EMAIL" -d "content=$RANDOM_CONTENT")

echo "Post response:"
echo "$POST_RESPONSE"

GET_RESPONSE=$(curl -s $API_URL)


echo "Get response:"
echo "$GET_RESPONSE"
