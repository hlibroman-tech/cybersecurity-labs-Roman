import hashlib
import base64
from cryptography.fernet import Fernet

class SimpleEmailEncryptor:
    def __init__(self, personal_data):
        """
        Ініціалізація класу.
        Генеруємо ключ на основі даних користувача (Email).
        """
        self.key = self._generate_key_from_data(personal_data)
        self.cipher = Fernet(self.key)
        
    def _generate_key_from_data(self, data):
        """
        Генерація ключа: хеш SHA-256 від пошти -> base64
        """
        digest = hashlib.sha256(data.encode()).digest()
        return base64.urlsafe_b64encode(digest)

    def encrypt_message(self, message):
        """Шифрування тексту"""
        encrypted_bytes = self.cipher.encrypt(message.encode())
        return encrypted_bytes.decode()

    def decrypt_message(self, encrypted_token):
        """Розшифрування тексту"""
        try:
            decrypted_bytes = self.cipher.decrypt(encrypted_token.encode())
            return decrypted_bytes.decode()
        except Exception as e:
            return f"Помилка: {e}"

# --- ОСНОВНА ЧАСТИНА (Інтерфейс як у першому варіанті) ---

def demo():
    print("=== Демонстрація захищеного обміну повідомленнями ===")
    
    # Крок 1: Генерація ключа
    print("\n[Крок 1] Генерація ключа на основі Email")
    # Встановлено вашу пошту як дефолтну
    email_input = input("Введіть Email: ")
    
    if not email_input:
        user_email = "hlib.roman@hneu.net"
    else:
        user_email = email_input
        
    encryptor = SimpleEmailEncryptor(user_email)
    print(f"-> Використано Email: {user_email}")
    print(f"-> Згенеровано унікальний ключ: {encryptor.key.decode()[:15]}...")

    # Крок 2: Введення повідомлення
    print("\n[Крок 2] Створення повідомлення")
    # Нове дефолтне повідомлення
    default_msg = "Лабораторна робота №5 виконана успішно. Оцінка: відмінно."
    msg_input = input(f"Введіть текст: ")
    
    if not msg_input:
        original_message = default_msg
    else:
        original_message = msg_input

    print(f"-> Оригінальний текст: {original_message}")

    # Крок 3: Шифрування
    print("\n[Крок 3] Шифрування повідомлення")
    encrypted_msg = encryptor.encrypt_message(original_message)
    print(f"-> Зашифровані дані (ciphertext):\n{encrypted_msg}")

    # Крок 4: Розшифрування
    print("\n[Крок 4] Розшифрування повідомлення отримувачем")
    decrypted_msg = encryptor.decrypt_message(encrypted_msg)
    print(f"-> Розшифрований текст: {decrypted_msg}")
    
    # Перевірка
    if original_message == decrypted_msg:
        print("\n[Успіх] Цілісність даних підтверджено.")
    else:
        print("\n[Помилка] Дані пошкоджено.")

if __name__ == "__main__":
    demo()