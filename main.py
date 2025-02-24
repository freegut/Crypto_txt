import os
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# Генерация ключа и вектора инициализации (IV)
def generate_key_iv(method):
    if method == "AES-256":
        key = os.urandom(32)  # 256-битный ключ для AES
        iv = os.urandom(16)   # 128-битный IV для AES
    elif method == "ChaCha20":
        key = os.urandom(32)  # 256-битный ключ для ChaCha20
        iv = os.urandom(16)   # 96-битный IV для ChaCha20
    else:
        raise ValueError("Неверный метод шифрования")
    return key, iv

# Шифрование данных
def encrypt_data(method, key, iv, plaintext):
    if method == "AES-256":
        # Добавляем padding к данным, чтобы они были кратны размеру блока
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        # Шифруем данные
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        tag = encryptor.tag
    elif method == "ChaCha20":
        # Шифруем данные с помощью ChaCha20
        cipher = Cipher(algorithms.ChaCha20(key, iv), mode=None, backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext)
        tag = None  # ChaCha20 не использует тэг аутентификации
    else:
        raise ValueError("Неверный метод шифрования")

    return ciphertext, tag

# Расшифрование данных
def decrypt_data(method, key, iv, ciphertext, tag=None):
    if method == "AES-256":
        # Расшифровываем данные
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # Убираем padding
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    elif method == "ChaCha20":
        # Расшифровываем данные с помощью ChaCha20
        cipher = Cipher(algorithms.ChaCha20(key, iv), mode=None, backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext)
    else:
        raise ValueError("Неверный метод шифрования")

    return plaintext

# Функция для шифрования файла
def encrypt_file():
    method = method_var.get()
    file_path = filedialog.askopenfilename(title="Выберите файл для шифрования")
    if not file_path:
        return

    key, iv = generate_key_iv(method)
    try:
        with open(file_path, "rb") as file:
            plaintext = file.read()
        ciphertext, tag = encrypt_data(method, key, iv, plaintext)

        # Перезаписываем исходный файл зашифрованными данными
        with open(file_path, "wb") as file:
            file.write(iv + ciphertext)
            if tag:
                file.write(tag)

        # Сохраняем ключ в отдельный файл .key
        key_file_path = file_path + ".key"
        with open(key_file_path, "wb") as key_file:
            key_file.write(key)

        messagebox.showinfo("Успех", f"Файл успешно зашифрован с использованием {method}!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось зашифровать файл: {e}")

# Функция для расшифрования файла
def decrypt_file():
    method = method_var.get()
    file_path = filedialog.askopenfilename(title="Выберите файл для расшифрования")
    if not file_path:
        return

    key_path = filedialog.askopenfilename(title="Выберите файл с ключом")
    if not key_path:
        return

    try:
        with open(file_path, "rb") as encrypted_file:
            data = encrypted_file.read()
        with open(key_path, "rb") as key_file:
            key = key_file.read()

        if method == "AES-256":
            iv = data[:16]
            ciphertext = data[16:-16]
            tag = data[-16:]
        elif method == "ChaCha20":
            iv = data[:16]
            ciphertext = data[16:]
            tag = None
        else:
            raise ValueError("Неверный метод шифрования")

        plaintext = decrypt_data(method, key, iv, ciphertext, tag)

        # Перезаписываем исходный файл расшифрованными данными
        with open(file_path, "wb") as file:
            file.write(plaintext)

        # Удаляем файл .key после успешного расшифрования
        os.remove(key_path)

        messagebox.showinfo("Успех", f"Файл успешно расшифрован с использованием {method}!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось расшифровать файл: {e}")

# Создаем графический интерфейс
def create_gui():
    global method_var

    root = tk.Tk()
    root.title("Шифрование и расшифрование файлов")
    root.geometry("400x200")

    # Выбор метода шифрования
    method_var = tk.StringVar(value="AES-256")
    aes_radio = tk.Radiobutton(root, text="AES-256", variable=method_var, value="AES-256")
    chacha_radio = tk.Radiobutton(root, text="ChaCha20", variable=method_var, value="ChaCha20")
    aes_radio.pack(pady=5)
    chacha_radio.pack(pady=5)

    # Кнопка для шифрования файла
    encrypt_button = tk.Button(root, text="Зашифровать файл", command=encrypt_file)
    encrypt_button.pack(pady=10)

    # Кнопка для расшифрования файла
    decrypt_button = tk.Button(root, text="Расшифровать файл", command=decrypt_file)
    decrypt_button.pack(pady=10)

    root.mainloop()

# Запуск программы
if __name__ == "__main__":
    create_gui()