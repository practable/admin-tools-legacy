#!/bin/bash

# Make token
export RELAY_TOKEN_LIFETIME=30
export RELAY_TOKEN_SCOPE_READ=true
export RELAY_TOKEN_SCOPE_WRITE=false
export RELAY_TOKEN_SECRET=$(cat ~/secret/v0/relay.pat)
export RELAY_TOKEN_TOPIC=stats
export RELAY_TOKEN_AUDIENCE=https://dev.practable.io/access
export client_token=$(relay token)
echo "client_token=${client_token}"

# Request Access
export ACCESS_URL="${RELAY_TOKEN_AUDIENCE}/session/stats"
echo $ACCESS_URL

export RESP=$(curl -X POST \
-H "Authorization: ${client_token}" \
				   $ACCESS_URL)

echo $RESP

