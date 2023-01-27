#!/bin/bash

# Make token
export ACCESSTOKEN_LIFETIME=30
export ACCESSTOKEN_ROLE=client
export ACCESSTOKEN_SECRET=$(cat ~/secret/v0/relay.pat)
export ACCESSTOKEN_TOPIC=stats
export ACCESSTOKEN_CONNECTIONTYPE=session
export ACCESSTOKEN_AUDIENCE=https://dev.practable.io
export client_token=$(relay token)
echo "client_token=${client_token}"

# Request Access
export ACCESS_URL="${ACCESSTOKEN_AUDIENCE}/access/session/stats"
echo $ACCESS_URL

export RESP=$(curl -X POST \
-H "Authorization: ${client_token}" \
				   $ACCESS_URL)

echo $RESP

