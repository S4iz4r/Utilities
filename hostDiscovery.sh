#!/bin/bash

if [[ $1 == *.*.*. ]]; then
	ip_address=$1
	for i in $(seq 2 254); do
		timeout 1 bash -c "ping -c 1 $ip_address$i > /dev/null  2>&1" && echo "Host $ip_address$i - ACTIVE" &
	done; wait
else
	echo -e "\n[*] Usage:  ./hostDyscovery.sh  <ip-address --.--.--.>\n"
	exit 1
fi

