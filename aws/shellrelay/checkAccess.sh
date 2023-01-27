#!/bin/sh

# Make token
export SHELLTOKEN_LIFETIME=30
export SHELLTOKEN_ROLE=stats
export SHELLTOKEN_SECRET=$(cat ~/secret/shellrelay.pat)
export SHELLTOKEN_TOPIC=stats
export SHELLTOKEN_CONNECTIONTYPE=shell
export SHELLTOKEN_AUDIENCE=https://shell-access.practable.io
export client_token=$(shellrelay token)
echo "client_token=${client_token}"

# Request Access
export ACCESS_URL="${SHELLTOKEN_AUDIENCE}/shell/stats"

curl -X POST  \
-H "Authorization: ${client_token}" \
$ACCESS_URL 

