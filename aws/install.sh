#!/bin/bash
go=$(which go)
if [ ! $? -eq 0 ]; then
   echo "please install go then try again"
fi

mkdir .cmd 2> /dev/null || true
mkdir bin 2> /dev/null || true
cd .cmd
if cd relay; then git pull origin v0.2.3; else git clone --branch v0.2.3 https://github.com/practable/relay && cd relay; fi
cd cmd/session
go build
cp session ../../../../bin/sessionrelay
cd ../shell
go build
cp shell ../../../../bin/shellrelay
cd ../book
go build
cp book ../../../../bin/book
