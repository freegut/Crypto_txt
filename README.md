This program provides a simple graphical interface for encrypting and decrypting files using modern encryption algorithms: **AES-256** and **ChaCha20**.

---

## Features

- Encrypt files using AES-256 or ChaCha20.
- Decrypt files using a saved key.
- User-friendly graphical interface built with `tkinter`.
- Automatic cleanup of temporary files after decryption.

---

## Requirements

- Python 3.7 or higher.
- Required libraries:
  - `cryptography`
  - `tkinter` (usually included with Python).

---

## Installation

1. Ensure Python is installed. You can download it from the [official website](https://www.python.org/downloads/).

2. Install the required libraries:

   ```bash
   pip install cryptography
   ```

3. Download the source code or clone the repository.

---

## Usage

1. Run the program:

   ```bash
   python main.py
   ```

2. Select an encryption method (AES-256 or ChaCha20).

3. Click "Encrypt File" and choose a file to encrypt. The program will overwrite the original file with encrypted data and create a key file (`.key`).

4. To decrypt, click "Decrypt File," select the encrypted file, and provide the key file (`.key`). The program will restore the original file and delete the key file.

---

## Compiling to an Executable (.exe)

1. Install PyInstaller:

   ```bash
   pip install pyinstaller
   ```

2. Navigate to the program's directory and run:

   ```bash
   pyinstaller --onefile --windowed main.py
   ```

3. The executable will be created in the `dist/` folder.

---

## Example Workflow

### Encrypting a File
1. Select an encryption method (e.g., AES-256).
2. Click "Encrypt File" and choose a file.
3. The program will create a key file (`.key`) and overwrite the original file with encrypted data.

### Decrypting a File
1. Click "Decrypt File."
2. Select the encrypted file and the key file (`.key`).
3. The program will restore the original file and delete the key file.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

freegut

---

## Support

If you have questions or encounter issues, please open an issue in the repository or contact me via email: guseiv2014@yandex.ru.

---

### Notes

- Ensure you securely store the key file (`.key`). Without it, decryption is impossible.
- The program overwrites the original file with encrypted data. If you need to keep the original, make a backup before encrypting.

---
