#!/bin/sh

# Make token
export SHELLTOKEN_LIFETIME=30
export SHELLTOKEN_ROLE=stats
export SHELLTOKEN_SECRET=$(cat ~/secret/shellrelay2.pat)
export SHELLTOKEN_TOPIC=stats
export SHELLTOKEN_CONNECTIONTYPE=shell
export SHELLTOKEN_AUDIENCE=https://shell-access2.practable.io
export client_token=$(shellrelay token)
echo "client_token=${client_token}"

# Request Access
export ACCESS_URL="${SHELLTOKEN_AUDIENCE}/shell/stats"

export STATS_URL=$(curl -X POST  \
-H "Authorization: ${client_token}" \
$ACCESS_URL | jq -r '.uri')

echo $STATS_URL
# Connect to stats channel & issue {"cmd":"update"}

echo '{"cmd":"update"}' | websocat -B 1048576 -n1 "$STATS_URL" | jq .
