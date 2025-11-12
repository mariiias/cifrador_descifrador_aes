#!/usr/bin/env python3
import sys
import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def derive_key_and_iv(password, salt, key_len=16, iv_len=16, iterations=10000):
    dk = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations,
        dklen=key_len + iv_len
    )
    return dk[:key_len], dk[key_len:] 

def encrypt(plaintext, password):
    if not plaintext:
        raise ValueError("El archivo a cifrar está vacío.")
    
    if password.strip() == "":
        raise ValueError("La contraseña no puede estar vacía.")

    salt = os.urandom(8)
    key, iv = derive_key_and_iv(password, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return b"Salted__" + salt + ciphertext

def decrypt(ciphertext, password):
    if not ciphertext:
        raise ValueError("El archivo de entrada está vacío.")
    
    if password.strip() == "":
        raise ValueError("La contraseña no puede estar vacía.")
    
    if not ciphertext.startswith(b"Salted__"):
        raise ValueError("Formato incorrecto o cabecera no encontrada.")
    
    salt = ciphertext[8:16]
    key, iv = derive_key_and_iv(password, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext[16:]), AES.block_size)
    return plaintext

def main():
    if len(sys.argv) != 3:
        sys.stderr.write("Uso: {} -e|-d <contraseña>\n".format(sys.argv[0]))
        sys.exit(1)

    mode = sys.argv[1]
    password = sys.argv[2]

    data_in = sys.stdin.buffer.read()

    try:
        if mode == "-e":
            data_out = encrypt(data_in, password)
        elif mode == "-d":
            data_out = decrypt(data_in, password)
        else:
            raise ValueError("Uso: ./xaes.py {-e|-d} <contraseña>")
    except Exception as e:
        sys.stderr.write("Error: {}\n".format(e))
        sys.exit(1)

    sys.stdout.buffer.write(data_out)

if __name__ == "__main__":
    main()

