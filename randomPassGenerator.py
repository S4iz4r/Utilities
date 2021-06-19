#!/usr/bin/python3
#coding: utf-8

import random
from time import time

lower = ("abcdefghijklmnopqrstuvwxyz")
upper = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
num = ("0123456789")
simb = ('!@#$%^&*()-_+=~[]{}|\':;<>,.?"/')

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

def split(password_characters):
    return list(password_characters)

if password_characters == "":
    password_characters = split(lower + upper + num + simb)
elif password_characters == "1":
    password_characters = split(lower)
elif password_characters == "2":
    password_characters = split(upper)
elif password_characters == "3":
    password_characters = split(num)
elif password_characters == "4":
    password_characters = split(lower + upper)
elif password_characters == "5":
    password_characters = split(upper + num)
else:
    password_characters = split(password_characters)

password = []
counter = 1
t1 = time()
def generator(password, password_length, dictionary_size, counter, password_characters):
	while counter <= dictionary_size:
		for i in range(password_length):
			password.append(random.choice(password_characters))
		data = "".join(map(str,password))
		counter += 1
		file.write(f"{data}\n")
		password = []

generator(password, password_length, dictionary_size, counter, password_characters)
t2 = time()
print(f"\nDictionary completed in {round(t2-t1,2)} seconds\n")

file.close()
