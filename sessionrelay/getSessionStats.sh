#!/bin/bash

# Make token
export ACCESSTOKEN_LIFETIME=30
export ACCESSTOKEN_ROLE=client
export ACCESSTOKEN_SECRET=$(cat ~/secret/sessionrelay.pat)
export ACCESSTOKEN_TOPIC=stats
export ACCESSTOKEN_CONNECTIONTYPE=session
export ACCESSTOKEN_AUDIENCE=https://relay-access.practable.io
export client_token=$(sessionrelay token)
echo "client_token=${client_token}"

# Request Access
export ACCESS_URL="${ACCESSTOKEN_AUDIENCE}/session/stats"
echo $ACCESS_URL

export RESP=$(curl -X POST \
-H "Authorization: ${client_token}" \
				   $ACCESS_URL)

echo $RESP

export STATS_URL=$(echo $RESP	| jq -r '.uri')

echo $STATS_URL
# Connect to stats channel & issue {"cmd":"update"}

echo '{"cmd":"update"}' | websocat -B 1048576 -n1 "$STATS_URL" | jq .
