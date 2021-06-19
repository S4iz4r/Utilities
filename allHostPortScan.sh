#!/bin/bash

function ctrl_c() {
    echo -e "\n[!] Exiting..."
    tput cnorm; exit 1
}
trap ctrl_c INT

tput civis

hosts=($@)

if [ $1 ]; then
    echo -e "\n[!] Hosts: ${hosts[@]}\n"
    for host in ${hosts[@]}; do
        echo -e "\n\t[>] $host\n"
        for port in $(seq 1 65535); do
            timeout 1 bash -c "echo '' > /dev/tcp/$host/$port"  2>/dev/null && echo "\t\t[*]$host ==> Port $port - OPEN"
        done
    done
else
    echo -e "\n[*] Usage:  ./allHostPortScan.sh  <ip-address> <ip-address> <ip-address> <ip-address> <ip-address>\n"
    tput cnorm
    exit 1
fi
tput cnorm
