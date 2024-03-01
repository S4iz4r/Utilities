#!/bin/bash
#Colours
greenColour="\e[0;32m\033[1m"
endColour="\033[0m\e[0m"
redColour="\e[0;31m\033[1m"
blueColour="\e[0;34m\033[1m"
yellowColour="\e[0;33m\033[1m"
purpleColour="\e[0;35m\033[1m"
turquoiseColour="\e[0;36m\033[1m"
grayColour="\e[0;37m\033[1m"

ports="$(cat $1 | grep -oP '\d{1,5}/open' | awk '{print $1}' FS='/' | xargs | tr ' ' ',')" 
ip_address="$(cat $1 | grep -oP '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' | sort -u | head -n 1)" 
echo -e "\n${yellowColour}[*] Extracting information...${endColour}\n" > extractPorts.tmp
echo -e "\t${blueColour}[*] IP Address:${endColour}${grayColour} $ip_address${endColour}" >> extractPorts.tmp
echo -e "\t${blueColour}[*] Open ports:${endColour}${grayColour} $ports${endColour}\n" >> extractPorts.tmp
echo "nmap -sC -sV -p"$ports $ip_address "-oN targeted" | tr -d '\n' | xclip -sel clip
echo -e "${yellowColour}[*] Ports copied to clipboard${endColour}\n" >> extractPorts.tmp
cat extractPorts.tmp
rm extractPorts.tmp
