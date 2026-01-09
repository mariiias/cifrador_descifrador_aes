# OpenSSL-Compatible Encryptor/Decryptor

> [Leer en Español](README.es.md) 🇪🇸

**System Tested:** Ubuntu 20.04 LTS

---

## Project Description

This project implements a **file encryptor and decryptor** using the **AES-128 algorithm in CBC (Cipher Block Chaining) mode**. It allows for secure file encryption and decryption using a user-provided password. The encryption key is derived using **PBKDF2 with HMAC-SHA256**, ensuring high security.

The program is **fully compatible with OpenSSL**, meaning you can encrypt files using OpenSSL and decrypt them with this software, and vice versa.

---

## Prerequisites

* **Python 3.10**
* **`venv` module** for creating virtual environments
* Required files:
  * `xaes.py`
  * `install.sh`
  * `requirements.txt`

---

## Installation

### Automatic Installation (Recommended)

1. Extract the project into a folder.
2. Open a terminal and navigate to that folder.
3. Run the following commands:

   ```bash
   chmod +x install.sh
   ./install.sh
   ```

   The script will automatically perform:
   * Verification of Python 3.10 and pip.
   * Creation and activation of the `venv` virtual environment.
   * Installation of dependencies (`pycryptodome`).
   * Execution permission assignment for `xaes.py`.

4. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

---

### Manual Installation

1. Extract the project.
2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Assign execution permissions to the script:

   ```bash
   chmod +x xaes.py
   ```

---

## Usage

The program is executed from the terminal via **stdin** and **stdout**. It can be used in combination with other command-line tools.

### Encrypt a File

```bash
cat original_file | ./xaes.py -e "my password" > encrypted_file
```

### Decrypt a File

```bash
cat encrypted_file | ./xaes.py -d "my password" > decrypted_file
```

**Integrity Check:**

```bash
diff original_file decrypted_file
```

If there is no output, the files are identical.

---

## OpenSSL Compatibility

You can verify interoperability between this program and OpenSSL:

### Encrypt with OpenSSL and Decrypt with `xaes.py`

```bash
cat original_file | openssl aes-128-cbc -pbkdf2 -k "my password" > encrypted_file
cat encrypted_file | ./xaes.py -d "my password" > decrypted_file
```

### Encrypt with `xaes.py` and Decrypt with OpenSSL

```bash
cat original_file | ./xaes.py -e "my password" > encrypted_file
cat encrypted_file | openssl aes-128-cbc -pbkdf2 -d -k "my password" > decrypted_file
```

---

## Technical Implementation

* **Algorithm:** AES-128-CBC
* **Key Derivation:** PBKDF2 with HMAC-SHA256 (10,000 iterations)
* **Encrypted File Format:**
  ```
  Salted__ + <8-byte salt> + <encrypted data>
  ```
* **Padding:** PKCS#7
* **Libraries:** `pycryptodome`, `hashlib`, `os`, `sys`

---

## Error Handling

* Empty file → `ValueError: "The file to encrypt is empty."`
* Empty password → `ValueError: "Password cannot be empty."`
* Incorrect format → `ValueError: "Incorrect format or header not found."`
* Incorrect parameters → Usage message displayed in the terminal.

---

## Test File

An **`archivo_prueba.txt`** file is included with the following text:

```
¡Hola, mundo!
```

### Usage Example:

```bash
cat archivo_prueba.txt | ./xaes.py -e my_password > encrypted_test_file
cat encrypted_test_file | ./xaes.py -d my_password > decrypted_test_file.txt
diff archivo_prueba.txt decrypted_test_file.txt
```

If there is no output, the encryption/decryption was successful.
