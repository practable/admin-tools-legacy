#!/bin/bash
EXPT=$1
export ACCESSTOKEN_LIFETIME=157680000
export ACCESSTOKEN_READ=true
export ACCESSTOKEN_WRITE=true
export ACCESSTOKEN_SECRET=$(cat ~/secret/sessionrelay.pat)
export ACCESSTOKEN_TOPIC=$EXPT
export ACCESSTOKEN_AUDIENCE=https://relay-access.practable.io
../bin/sessionrelay token

