#!/bin/bash

function ctrl_c() {
    echo -e "\n[!] Exiting..."
    tput cnorm; exit 1
}
trap crtl_c INT

tput civis

hosts=($1 $2 $3 $4 $5)

if [ $1 ]; then
    for host in ${hosts[@]}; do
        for port in $(seq 1 65535); do
            timeout 1 bash -c "echo '' > /dev/tcp/$host/$port"  2>/dev/null && echo "[*]$host ==
> Port $port - OPEN" &
        done; wait
    done
else
    echo -e "\n[*] Uso:  ./allHostPortScan.sh  <ip-address> <ip-address> <ip-address> <ip-address> <ip-address>\n"
    tput cnorm
    exit 1
fi
tput cnorm
