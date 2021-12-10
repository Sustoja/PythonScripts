
# Descifra un fichero suministrado por el usuario
# La clave simetrica de descifrado debe estar en el fichero 'filekey.key'
#
# IMPORTANTE: Si se pierde la clave sera imposible descifrar
#
# https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/

# import required module
from cryptography.fernet import Fernet

# opening the key
with open('filekey.key', 'rb') as filekey:
	key = filekey.read()

# using the key
fernet = Fernet(key)

# opening the encrypted file
filename = input("Fichero a descifrar: ")
with open(filename, 'rb') as enc_file:
	encrypted = enc_file.read()

# decrypting the file
decrypted = fernet.decrypt(encrypted)

# writing the decrypted data
with open(filename, 'wb') as dec_file:
	dec_file.write(decrypted)

