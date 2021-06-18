#!/bin/bash

function ctrl_c() {
	echo -e "\n[!] Exiting..."
	tput cnorm; exit 1
}
trap crtl_c INT

tput civis

hosts=(172.18.0.1 172.18.0.2 172.18.0.3 172.18.0.4)

for host in ${hosts[@]}; do
	for port in $(seq 1 200); do
		timeout 1 bash -c "echo '' > /dev/tcp/$host/$port"  2>/dev/null && echo "[*]$host ==> Port $port - OPEN" &
	done; wait
done
