#!/usr/bin/env python3
import sys
import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Deriva clave e IV de la contraseña y la sal usando PBKDF2 con HMAC-SHA256.
def derive_key_and_iv(password, salt, key_length=16, iv_length=16, iterations=600000):
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations, dklen=key_length + iv_length)
    return dk[:key_length], dk[key_length:]

# Función para cifrar
def encrypt(data, password):
    # Genera 8 bytes de sal aleatoria
    salt = os.urandom(8)
    key, iv = derive_key_and_iv(password, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Se aplica padding para que los datos sean múltiplos del tamaño de bloque (16 bytes)
    encrypted = cipher.encrypt(pad(data, AES.block_size))
    return b"Salted__" + salt + encrypted

# Función para descifrar
def decrypt(data, password):
    # Comprueba la cabecera "Salted__"
    if data[:8] != b"Salted__":
        raise ValueError("Formato incorrecto: no se encontró la cabecera 'Salted__'.")
    salt = data[8:16]
    key, iv = derive_key_and_iv(password, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Se descifra y se elimina el padding
    decrypted = unpad(cipher.decrypt(data[16:]), AES.block_size)
    return decrypted

def main():
    # Verifica que se hayan pasado exactamente dos argumentos: opción y contraseña
    if len(sys.argv) != 3:
        sys.stderr.write("Uso: {} -e|-d contraseña\n".format(sys.argv[0]))
        sys.exit(1)

    mode = sys.argv[1]
    password = sys.argv[2]
    data = sys.stdin.buffer.read()

    try:
        if mode == "-e":
            output = encrypt(data, password)
        elif mode == "-d":
            output = decrypt(data, password)
        else:
            sys.stderr.write("Opción desconocida: use -e para cifrar o -d para descifrar.\n")
            sys.exit(1)
    except Exception as e:
        sys.stderr.write("Error: {}\n".format(e))
        sys.exit(1)

    sys.stdout.buffer.write(output)

if __name__ == '__main__':
    main()
