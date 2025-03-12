#!/usr/bin/env python3
import sys
import subprocess


def main():
    if len(sys.argv) != 3:
        sys.stderr.write("Uso: {} -e|-d contraseña\n".format(sys.argv[0]))
        sys.exit(1)

    mode = sys.argv[1]
    password = sys.argv[2]

    data = sys.stdin.buffer.read()

    if mode == '-e':
        openssl_mode = '-e'
    elif mode == '-d':
        openssl_mode = '-d'
    else:
        sys.stderr.write("Opción desconocida: use -e para cifrar o -d para descifrar.\n")
        sys.exit(1)

    cmd = ['openssl', 'aes-128-cbc', '-pbkdf2', openssl_mode, '-k', password]

    try:
        result = subprocess.run(cmd, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        sys.stderr.write("Error al ejecutar OpenSSL: {}\n".format(e))
        sys.exit(1)

    if result.returncode != 0:
        sys.stderr.write("Error en OpenSSL: {}\n".format(result.stderr.decode()))
        sys.exit(1)

    sys.stdout.buffer.write(result.stdout)


if __name__ == '__main__':
    main()
