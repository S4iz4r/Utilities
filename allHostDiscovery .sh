#!/bin/bash

function ctrl_c() {
    echo -e "\n[!] Exiting..."
    exit 1
}
trap ctrl_c INT

if [[ $1 == *.*.*. ]] && [[ $2 ]]; then
	ip_address=$1
	interface=$2
	for s in $(seq $(echo "$1" | awk '{print $1}' FS='.') 254); do
		for r in $(seq $(echo "$1" | awk '{print $2}' FS='.') 254); do
			for a in $(seq $(echo "$1" | awk '{print $3}' FS='.') 254); do
				for i in $(seq 1 254); do
					timeout 1 bash -c "ping -c 1 -I $interface $s.$r.$a.$i > /dev/null  2>&1" && echo "Host $s.$r.$a.$i - ACTIVE" &
				done
			done
		done
	done; wait
else
	echo -e "\n[*] Use:  allHostDyscovery.sh  <ip-address --.--.--.> <interface> [!] Example: hostDiscovery.sh 127.0.0. eth0\n"
	exit 1
fi

