#!/bin/bash

function ctrl_c() {
    echo -e "\n[!] Exiting..."
    tput cnorm; exit 1
}
trap ctrl_c INT
tput civis

if [[ $1 == *.*.*. ]] && [[ $2 ]]; then
    ip_address=$1
    hosts=()
    echo -e "[*] Scanning Hosts for $ip_address??"
    hosts+=($(for i in $(seq 2 254); do timeout 1 bash -c "ping -c 1 -I $2 $ip_address$i > /dev/null  2>&1" && echo "$ip_address$i" & done; wait))
    echo -e "\n[*] Detected active hosts:\n $(for i in ${hosts[@]}; do echo -e "\t\t$i"; done)\n"
    echo -e "\t[*] Scanning ports"
    for host in ${hosts[@]}; do
        echo -e "\t\t[>] $host"
        for port in $(seq 1 1000); do
            timeout 1 bash -c "echo '' > /dev/tcp/$host/$port" 2>/dev/null && echo -e "\t\t\t[*] $host ==> Port $port - OPEN" 
        done  
    done
else
    echo -e "\n[!] Usage:  HostandPortDiscovery.sh  <ip-address --.--.--.> <interface>\n"
    echo -e "\n[!] Example: ./HostandPortDiscovery.sh 10.10.10. tun0\n"
    tput cnorm; exit 1
fi

tput cnorm
