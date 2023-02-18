#!/bin/bash
sshpass=$(which sshpass)
if [ ! $? -eq 0 ]; then
   echo "please install sshpass then try again"
fi

go=$(which go)
if [ ! $? -eq 0 ]; then
   echo "please install go then try again"
fi

mkdir .source 2> /dev/null || true
mkdir bin 2> /dev/null || true
cd .source
if cd relay 2> /dev/null; then git pull origin v0.2.3; else git clone --branch v0.2.3 https://github.com/practable/relay && cd relay; fi
cd cmd/session
go build
cp session ../../../../bin/sessionrelay
cd ../shell
go build
cp shell ../../../../bin/shellrelay
cd ../book
go build
cp book ../../../../bin/book

## Make the legacy version of shellrelay (incompatible with new version because it expects a token audience that is not an array)
cd ../..
git checkout v0.2.0
cd cmd/shell
go build
cp shell ../../../../bin/shellrelay-legacy
