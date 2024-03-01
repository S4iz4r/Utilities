#!/usr/bin/python3
# coding: utf-8

import random
import time
import string
from datetime import datetime


def generator(password_characters, password_length):
    data = "".join(random.choices(
        password_characters, k=password_length))
    return data


def main():
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

    print(f"\nTask started at: {str(datetime.now().strftime('%H:%M:%S'))}")
    t1 = time.time()
    data = (generator(password_characters, password_length)
            for _ in range(dictionary_size))
    file.write("\n".join(data))
    t2 = time.time()
    print(
        f"\nDictionary completed in {round(t2-t1, 2)} seconds.  {int(dictionary_size / round(t2-t1, 2))} words per second\n")
    print(f"Task completed at: {str(datetime.now().strftime('%H:%M:%S'))}\n")
    file.close()


if __name__ == '__main__':
    main()
