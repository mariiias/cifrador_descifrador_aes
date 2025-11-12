
# Cifrador/Descifrador Compatible con OpenSSL


**Sistema probado:** Ubuntu 20.04 LTS

---

## Descripción del proyecto

Este proyecto implementa un **cifrador y descifrador de archivos** utilizando el algoritmo **AES-128 en modo CBC (Cipher Block Chaining)**.
Permite cifrar y descifrar archivos de manera segura usando una contraseña proporcionada por el usuario, derivando la clave de cifrado mediante **PBKDF2 con HMAC-SHA256**, garantizando así una alta seguridad.

El programa es **totalmente compatible con OpenSSL**, lo que permite cifrar con OpenSSL y descifrar con este software, y viceversa.

---

## Requisitos previos

* **Python 3.10**
* **Módulo `venv`** para crear entornos virtuales
* Archivos necesarios:

  * `xaes.py`
  * `install.sh`
  * `requirements.txt`

---

## Instalación

### Instalación automática (recomendada)

1. Descomprime el proyecto en una carpeta.

2. Abre una terminal y navega a dicha carpeta.

3. Ejecuta los siguientes comandos:

   ```bash
   chmod +x install.sh
   ./install.sh
   ```

   El script realizará automáticamente:

   * Verificación de Python 3.10 y pip
   * Creación y activación del entorno virtual `venv`
   * Instalación de dependencias (`pycryptodome`)
   * Asignación de permisos de ejecución a `xaes.py`

4. Activa el entorno virtual:

   ```bash
   source venv/bin/activate
   ```

---

### Instalación manual

1. Descomprime el proyecto.

2. Crea un entorno virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Asigna permisos al script:

   ```bash
   chmod +x xaes.py
   ```

---

## Uso del programa

El programa se ejecuta desde la terminal mediante **stdin** y **stdout**.
Se puede usar en combinación con otras herramientas de línea de comandos.

### 🔹 Cifrar un archivo

```bash
cat archivo_original | ./xaes.py -e "mi contraseña" > archivo_cifrado
```

### 🔹 Descifrar un archivo

```bash
cat archivo_cifrado | ./xaes.py -d "mi contraseña" > archivo_descifrado
```

Comprobación de integridad:

```bash
diff archivo_original archivo_descifrado
```

Si no hay salida, los archivos son idénticos.

---

## Compatibilidad con OpenSSL

Puedes comprobar la interoperabilidad entre este programa y OpenSSL:

### 🔹 Cifrar con OpenSSL y descifrar con `xaes.py`

```bash
cat archivo_original | openssl aes-128-cbc -pbkdf2 -k "mi contraseña" > archivo_cifrado
cat archivo_cifrado | ./xaes.py -d "mi contraseña" > archivo_descifrado
```

### 🔹 Cifrar con `xaes.py` y descifrar con OpenSSL

```bash
cat archivo_original | ./xaes.py -e "mi contraseña" > archivo_cifrado
cat archivo_cifrado | openssl aes-128-cbc -pbkdf2 -d -k "mi contraseña" > archivo_descifrado
```

---

## Implementación técnica

* **Algoritmo:** AES-128-CBC
* **Derivación de clave:** PBKDF2 con HMAC-SHA256 (10.000 iteraciones)
* **Formato del archivo cifrado:**

  ```
  Salted__ + <8 bytes de sal> + <datos cifrados>
  ```
* **Padding:** PKCS#7
* **Librerías:** `pycryptodome`, `hashlib`, `os`, `sys`

---

## Manejo de errores

* Archivo vacío → `ValueError: "El archivo a cifrar está vacío."`
* Contraseña vacía → `ValueError: "La contraseña no puede estar vacía."`
* Formato incorrecto → `ValueError: "Formato incorrecto o cabecera no encontrada."`
* Parámetros incorrectos → Mensaje de uso mostrado en terminal

---

## Archivo de prueba

Se incluye un archivo **`archivo_prueba.txt`** con el texto:

```
¡Hola, mundo!
```

### Ejemplo de uso:

```bash
cat archivo_prueba.txt | ./xaes.py -e mi_contraseña > archivo_prueba_cifrado
cat archivo_prueba_cifrado | ./xaes.py -d mi_contraseña > archivo_prueba_descifrado.txt
diff archivo_prueba.txt archivo_prueba_descifrado.txt
```

Si no hay salida, el cifrado/descifrado ha sido exitoso 

