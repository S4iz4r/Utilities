#!/usr/bin/python3
#coding: utf-8

import random
from time import time

minus = ("abcdefghijklmnopqrstuvwxyz")
mayus = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
num = ("0123456789")
simb = ('!@#$%^&*()-_+=~[]{}|\':;<>,.?"/')

nombre_archivo = str(input("\nIntroduzca un nombre para su diccionario: "))
fichero = open(f"{nombre_archivo}.txt", "w")
password_length = int(input("\nIntroduzca la longitud de la contraseña: "))
tamaño_diccionario = int(input("\nIntroduzca la cantidad de contraseñas que desea generar: "))
password_characters = str(input("""
    \nIntroduzca los caracteres que comporndrán la contraseña:
Opciones:
1 - Sólo minúsculas
2 - Sólo mayúsculas
3 - Sólo números
4 - Combinación de las opciones 1 y 2
5 - Combinación de las opciones 2 y 3
Deje el campo vacío para usar todas las combinaciones (símbolos incuidos)
o introduzca su propia lista de caracteres: """))

def split(password_characters):
    return list(password_characters)

if password_characters == "":
    password_characters = split(minus + mayus + num + simb)
elif password_characters == "1":
    password_characters = split(minus)
elif password_characters == "2":
    password_characters = split(mayus)
elif password_characters == "3":
    password_characters = split(num)
elif password_characters == "4":
    password_characters = split(minus + mayus)
elif password_characters == "5":
    password_characters = split(mayus + num)
else:
    password_characters = split(password_characters)

password = []
contador = 1
t1 = time()
def generator(password, password_length, tamaño_diccionario, contador, password_characters):
	while contador <= tamaño_diccionario:
		for i in range(password_length):
			password.append(random.choice(password_characters))
		datos = "".join(map(str,password))
		contador += 1
		fichero.write(f"{datos}\n")
		password = []

generator(password, password_length, tamaño_diccionario, contador, password_characters)
t2 = time()
print(f"\nDiccionario finalizado en {round(t2-t1,2)} segundos\n")

fichero.close()
