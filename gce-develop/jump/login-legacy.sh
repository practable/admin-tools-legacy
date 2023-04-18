#!/bin/bash

# Usage ./login <expt_id>
# Example ./login pend00
export EXPT=$1

function freeport(){
 #https://unix.stackexchange.com/questions/55913/whats-the-easiest-way-to-find-an-unused-local-port
 port=$(comm -23 <(seq 49152 65535 | sort) <(ss -Htan | awk '{print $4}' | cut -d':' -f2 | sort -u) | sort -n | head -n 1)
}

freeport

export SHELLTOKEN_LIFETIME=86400
export SHELLTOKEN_ROLE=client
export SHELLTOKEN_SECRET=$(cat ~/secret/shellrelay.pat)
export SHELLTOKEN_CONNECTIONTYPE=shell
export SHELLTOKEN_AUDIENCE=https://shell-access.practable.io
export SHELLTOKEN_TOPIC=$EXPT
export SHELLCLIENT_TOKEN=$(../bin/shellrelay token)
export SHELLCLIENT_LOCALPORT="${port}"
export SHELLCLIENT_RELAYSESSION="${SHELLTOKEN_AUDIENCE}/${SHELLTOKEN_CONNECTIONTYPE}/${SHELLTOKEN_TOPIC}"
export SHELLCLIENT_DEVELOPMENT=true

../bin/shellrelay-legacy client >/dev/null 2>&1 &
pid=$!
export SSHPASS=$(~/secret/ep $EXPT)
user=$(~/secret/eu $EXPT)
sshpass -v -e ssh -o "StrictHostKeyChecking no" "${user}@localhost" -p "$port" 
kill $!



