# Cifra un fichero suministrado por el usuario
# y guarda la clave simetrica en 'filekey.key'
#
# IMPORTANTE: Si se pierde la clave sera imposible descifrar
#
# https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/


# import required module
from cryptography.fernet import Fernet

# key generation
key = Fernet.generate_key()

# save the key in a file
with open('filekey.key', 'wb') as filekey:
    filekey.write(key)

# opening the key
with open('filekey.key', 'rb') as filekey:
    key = filekey.read()

# using the generated key
fernet = Fernet(key)

# opening the file to encrypt
filename = input("Fichero a cifrar: ")
with open(filename, 'rb') as file:
    original = file.read()

# encrypting the file
encrypted = fernet.encrypt(original)

# writing the encrypted data
with open(filename, 'wb') as encrypted_file:
    encrypted_file.write(encrypted)
