#!/bin/bash

# user-token.sh helps creates booking tokens
# example usage: user-token.sh "https://book.practable.io" "truss everyone" 2122-10-12T07:20:50Z 86400
export BOOKTOKEN_SECRET=$(cat ~/secret/book.pat)
export BOOKTOKEN_AUDIENCE=$1
export BOOKTOKEN_GROUPS=$2
export BOOKTOKEN_NBF=$3
export BOOKTOKEN_LIFETIME=$4
export BOOKTOKEN_ADMIN=false
export USERTOKEN=$(../bin/book token)
echo ${USERTOKEN}

