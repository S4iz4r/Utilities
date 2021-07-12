#!/usr/bin/python3
# coding: utf-8

import string
import random
from time import time


file_name = str(input("\nEnter name for dictionary: "))
file = open(f"{file_name}.txt", "w")
password_length = int(input("\nEnter length for password: "))
dictionary_size = int(input("\nEnter the number of passwords: "))
password_characters = str(input("""
    \nEnter the characters that will make up the password:
Options:
1 - Only lowercase
2 - Only uppercase
3 - Only numbers
4 - Combination of options 1 and 2
5 - Combination of options 2 and 3
Leave the field empty to use all combinations (symbols included)
or enter your own character list: """))


if password_characters == "":
    password_characters = (
            string.ascii_lowercase +
            string.ascii_uppercase +
            string.punctuation
            )
elif password_characters == "1":
    password_characters = string.ascii_lowercase
elif password_characters == "2":
    password_characters = string.ascii_uppercase
elif password_characters == "3":
    password_characters = string.digits
elif password_characters == "4":
    password_characters = string.ascii_letters
elif password_characters == "5":
    password_characters = string.ascii_uppercase + string.digits
else:
    password_characters = password_characters


def generator(password_length, password_characters):
    password = []
    for i in range(password_length):
        password.append(random.choice(password_characters))
    file.write(f"{''.join(map(str, password))}\n")
    password = []


t1 = time()
for _ in range(dictionary_size):
    generator(password_length, password_characters)
t2 = time()
print(f"\nDictionary completed in {round(t2-t1,2)} seconds\n")
file.close()
