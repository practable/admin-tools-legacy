#!/bin/bash

# serve.sh is a script to help with loading
# and resetting the manifest at
# dev.practable.io/book

# pad base64URL encoded to base64
# from https://gist.github.com/angelo-v/e0208a18d455e2e6ea3c40ad637aac53
paddit() {
  input=$1
  l=`echo -n $input | wc -c`
  while [ `expr $l % 4` -ne 0 ]
  do
    input="${input}="
    l=`echo -n $input | wc -c`
  done
  echo $input
}

if [ "$BOOK_ADMIN_SECRET" = "" ];
then
	echo 'you must set BOOK_ADMIN_SECRET'
fi

export BOOK_CLIENT_HOST=dev.practable.io
export BOOK_CLIENT_BASE_PATH=/book/api/v1
export BOOK_CLIENT_SCHEME=https
export BOOK_CLIENT_SECRET=$(cat ~/secret/v0/book.pat)
export BOOK_CLIENT_TOKEN_AUD=https://dev.practable.io/book
export BOOK_CLIENT_TOKEN_TTL=5m
export BOOK_CLIENT_TOKEN_ADMIN=true
export BOOK_CLIENT_TOKEN_SUB=admin
export BOOK_CLIENT_TOKEN=$(../bin/book token)
echo "Admin token:"
echo ${BOOK_CLIENT_TOKEN}

# read and split the token and do some base64URL translation
read h p s <<< $(echo $BOOKCLIENT_TOKEN | tr [-_] [+/] | sed 's/\./ /g')

h=`paddit $h`
p=`paddit $p`
# assuming we have jq installed
echo $h | base64 -d | jq
echo $p | base64 -d | jq

set | grep BOOKCLIENT


echo "book server at ${BOOKCLIENT_HOST} (testing)"

echo "commands:"
echo
echo "  0: Get status"
echo "  1: Lock bookings"
echo "  2: Unlock bookings"
echo 
echo "  3: Export bookings"
echo "  4: Replace bookings"
echo 
echo "  5: Export old bookings"
echo "  6: Replace old bookings"
echo 
echo "  7: Check manifest"
echo "  8: Export manifest"
echo "  9: Replace manifest (JSON)"
echo "  a: Replace manifest (YAML)"
echo 
echo "  b: Export users"
echo "  c: start insecure chrome"

for (( ; ; ))
do
	read -p 'What next? ' command
if [ "$command" = "0" ];
then
 	../bin/book status get
	#not working curl -X GET -H "Authorization: ${BOOKCLIENT_TOKEN}" "${BOOK_CLIENT_SCHEME}://${BOOK_CLIENT_HOST}${BOOK_CLIENT_BASE_PATH}/admin/status"
	
elif [ "$command" = "1" ];
then
	read -p 'Enter lock message:' message
	../bin/book status set lock "$message"
elif [ "$command" = "2" ];
then
	read -p 'Enter unlock message:' message
	../bin/book status set unlock "$message"
elif [ "$command" = "3" ];
then
	#export BOOKCLIENT_FORMAT=yaml
	#../bin/book bookings export
	curl -X GET -H "Authorization: ${BOOK_CLIENT_TOKEN}" "${BOOK_CLIENT_SCHEME}://${BOOK_CLIENT_HOST}${BOOK_CLIENT_BASE_PATH}/admin/bookings" > exported_bookings.json
elif [ "$command" = "4" ];
then
	read -p "Definitely replace [y/N]?" confirm
	if ([ "$confirm" == "y" ] || [ "$confirm" == "Y" ]  || [ "$confirm" == "yes"  ] );
	then
		#../bin/book bookings replace ../demo/bookings.yaml #boiler plate code doesn't report the error messages (just get pointer values) ... :-(
		curl --data-binary "@./generated_bookings.json"  -X PUT -H "Authorization: ${BOOK_CLIENT_TOKEN}" -H "Content-type: application/json" "${BOOK_CLIENT_SCHEME}://${BOOK_CLIENT_HOST}${BOOK_CLIENT_BASE_PATH}/admin/bookings" 
	fi

elif [ "$command" = "5" ];
then
	export BOOKCLIENT_FORMAT=yaml
	../bin/book oldbookings export
elif [ "$command" = "6" ];
then
	read -p "Definitely replace [y/N]?" confirm
	if ([ "$confirm" == "y" ] || [ "$confirm" == "Y" ]  || [ "$confirm" == "yes"  ] );
	then	
	    echo "replace old bookings"
	fi	

elif [ "$command" = "7" ];
then
	../bin/book manifest check ../demo/manifest.yaml
elif [ "$command" = "8" ];
then
	export BOOKCLIENT_FORMAT=yaml
	../bin/book manifest export 
elif [ "$command" = "9" ];
then
	read -p "Definitely replace [y/N]?" confirm
	if ([ "$confirm" == "y" ] || [ "$confirm" == "Y" ]  || [ "$confirm" == "yes"  ] );
	then
	        export BOOKCLIENT_FORMAT=json
	    	../bin/book manifest replace ../demo/manifest.json
	fi

elif [ "$command" = "a" ];
then
    		export BOOKCLIENT_FORMAT=yaml
		../bin/book manifest replace ../demo/manifest2.yaml
		
elif [ "$command" = "b" ];
then
    		
	echo "export users"
elif [ "$command" = "c" ];
then	
	mkdir -p ~/tmp/chrome-user
	google-chrome --disable-web-security --user-data-dir="~/tmp/chrome-user" > chrome.log 2>&1 &
else	
     echo -e "\nUnknown command ${command}."
fi
done

kill book_pid



