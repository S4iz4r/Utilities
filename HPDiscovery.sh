#!/bin/bash

function ctrl_c() {
    echo -e "\n[!] Exiting..."
    tput cnorm; exit 1
}
trap ctrl_c INT
tput civis

portRangeStart=1
portRange=5000

if [[ $3 ]] && [[ -z $4 ]]; then
    portRange=$3
elif [[ $3 ]] && [[ $4 ]]; then
    portRangeStart=$3
    portRange=$4
fi

if [[ $1 == *.*.*. ]] && [[ $2 ]]; then
    ip_address=$1
    hosts=()
    echo -e "[*] Scanning Hosts for $ip_address??"
    hosts+=($(for i in $(seq 2 254); do timeout 0.5 bash -c "ping -c 1 -I $2 $ip_address$i > /dev/null  2>&1" && echo "$ip_address$i" & done; wait))
    echo -e "\n[*] Detected active hosts:\n $(for i in ${hosts[@]}; do echo -e "\t\t$i"; done)\n"
    echo -e "[*] Scanning open ports     [[   from port   $portRangeStart   to port   $portRange   ]]"
    sleep 2
    for host in ${hosts[@]}; do
        if [[ $host != $(/usr/sbin/ifconfig $2 | grep "inet " | awk '{print $2}') ]]; then
            ttl=$(bash -c "ping -c 1 -I $2 $host | grep ttl= | awk -F= '{print \$3,\$4}' | sed 's/ //3; s/time/ /' 2>&1") && echo -e "\n$host   ttl=${ttl}\n"
            for port in $(seq $portRangeStart $portRange); do
                timeout 0.5 bash -c "echo '' > /dev/tcp/$host/$port" 2>/dev/null && echo -e "\t\tPort $port" &
            done; wait
        fi
    done
else
    echo -e "\n[!] Usage:  ./HPDiscovery.sh  <ip-address --.--.--.> <interface> <start port> <finish port>"
    echo -e "\n[!] Port scanner range set from 1 to 5000 by deffault"
    echo -e "\n[!] Example: ./HPDiscovery.sh 127.0.0. eth0"
    echo -e "\n[!] Example: ./HPDiscovery.sh 127.0.0. eth0 65535"
    echo -e "\n[!] Example: ./HPDiscovery.sh 127.0.0. eth0 1000 5000\n"
    tput cnorm; exit 1
fi

tput cnorm
