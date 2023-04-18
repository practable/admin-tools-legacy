#/bin/bash

#example ./book-token-lifetime.sh "recruit everyone"  172800

if [ "$BOOK_SECRET" = "" ];
then
	echo 'you must set BOOK_SECRET'
fi

export BOOKTOKEN_SECRET=$(cat ~/secret/book.pat)
export BOOKTOKEN_AUDIENCE=https://book.practable.io
export BOOKTOKEN_LIFETIME=$2
export BOOKTOKEN_GROUPS=$1
export BOOKTOKEN_ADMIN=true
export BOOKUPLOAD_TOKEN=$(../bin/book token)
echo "Admin token:"
echo ${BOOKUPLOAD_TOKEN}
echo ${BOOKUPLOAD_TOKEN}| decode-jwt

# generate user token
export BOOKTOKEN_ADMIN=false
export USERTOKEN=$(book token)
export BOOKJS_USERTOKEN=$(../bin/book token)
echo "User token:"
echo ${BOOKJS_USERTOKEN}
echo ${BOOKJS_USERTOKEN} | decode-jwt
