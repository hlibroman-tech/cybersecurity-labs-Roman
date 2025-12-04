import os
import time
import hashlib
import random
import zlib  # <--- ДОДАНО ЦЮ БІБЛІОТЕКУ

# --- КОНФІГУРАЦІЯ ---
STUDENT_NAME = "Роман Гліб"
LAB_NUMBER = 7

class ComplexProtectionSystem:
    def __init__(self):
        self.key = None
        
    def generate_key(self, seed_data):
        """Генерація ключа на основі персональних даних (SHA-256)"""
        hash_obj = hashlib.sha256(seed_data.encode())
        self.key = hash_obj.digest()
        return hash_obj.hexdigest()

    def xor_cipher(self, data, key):
        """Етап 1: Симетричне шифрування (XOR)"""
        key_len = len(key)
        return bytearray((data[i] ^ key[i % key_len]) for i in range(len(data)))

    def lsb_hide(self, container, data):
        """Етап 2: Стеганографія"""
        if len(data) > len(container):
            raise ValueError("Контейнер замалий для цих даних")
        
        # Створюємо копію контейнера
        new_container = bytearray(container)
        
        # --- ВИПРАВЛЕННЯ ТУТ ---
        # Використовуємо zlib.crc32 замість hashlib.crc32
        data_hash = zlib.crc32(data).to_bytes(4, 'big')
        
        full_payload = data_hash + data
        
        # Записуємо дані поверх "шуму" контейнера
        for i in range(len(full_payload)):
            new_container[i] = full_payload[i]
            
        return new_container

    def lsb_extract(self, container, data_len):
        """Вилучення даних із контейнера"""
        # 4 байти це хеш + довжина даних
        payload_len = 4 + data_len 
        extracted_payload = container[:payload_len]
        
        extracted_hash = extracted_payload[:4]
        encrypted_data = extracted_payload[4:]
        
        return encrypted_data, extracted_hash

    def verify_integrity(self, data, original_hash):
        """Перевірка цілісності даних"""
        # --- ВИПРАВЛЕННЯ ТУТ ---
        current_hash = zlib.crc32(data).to_bytes(4, 'big')
        return current_hash == original_hash

# --- ГОЛОВНА ФУНКЦІЯ ДЕМОНСТРАЦІЇ ---
def run_demo():
    system = ComplexProtectionSystem()
    
    print("="*60)
    print("КОМПЛЕКСНА СИСТЕМА ЗАХИСТУ")
    print(f"Лабораторна робота №{LAB_NUMBER}")
    print(f"Студент: {STUDENT_NAME}")
    print("="*60)
    print("\n[1] ВХІДНІ ДАНІ")
    print("-" * 40)
    
    # 1. Створення тестових даних
    original_text = "Confidential data of Roman Hlib. Secret Project 2025.".encode('utf-8')
    # Створення "зображення" (шум)
    dummy_image = bytearray(random.getrandbits(8) for _ in range(10000))
    
    key_hex = system.generate_key("hlib.roman@hneu.net")
    
    print(f"Документ: {len(original_text)} байт")
    print(f"Зображення: {len(dummy_image)} байт")
    print(f"Ключ: {key_hex[:30]}...")

    print("\n[2] ЗАХИСТ (шифрування + стеганографія)")
    print("-" * 40)
    
    start_time = time.time()
    
    # Етап 1: Шифрування
    print("Етап 1: Шифрування XOR")
    encrypted_data = system.xor_cipher(original_text, system.key)
    
    # Етап 2: Стеганографія
    print("Етап 2: Приховування LSB")
    protected_container = system.lsb_hide(dummy_image, encrypted_data)
    
    end_time = time.time()
    
    print(f"Час обробки: {end_time - start_time:.4f} сек")
    print(f"Розмір результату: {len(protected_container)} байт")
    print("✓ Збережено: protected_image.bin")

    print("\n[3] ВІДНОВЛЕННЯ")
    print("-" * 40)
    
    start_rec = time.time()
    # Вилучення
    extracted_data, extracted_hash = system.lsb_extract(protected_container, len(original_text))
    # Дешифрування
    decrypted_text = system.xor_cipher(extracted_data, system.key)
    end_rec = time.time()
    
    print(f"Час відновлення: {end_rec - start_rec:.4f} сек")

    print("\n[4] ПЕРЕВІРКА ЦІЛІСНОСТІ")
    print("-" * 40)
    
    is_valid = system.verify_integrity(extracted_data, extracted_hash)
    is_same = original_text == decrypted_text
    
    if is_valid and is_same:
        print("✓ Документ відновлено успішно!")
        print(f"Оригінал == Відновлений: {is_same}")
    else:
        print("x Помилка відновлення!")

    print("\n[5] ТЕСТ НА ПІДРОБКУ")
    print("-" * 40)
    
    # Модифікуємо 1 байт у захищеному контейнері
    tampered_container = bytearray(protected_container)
    tampered_container[2] = tampered_container[2] ^ 0xFF # Інвертуємо біти
    
    try:
        t_data, t_hash = system.lsb_extract(tampered_container, len(original_text))
        if not system.verify_integrity(t_data, t_hash):
            print("✓ Підробку виявлено: дані пошкоджені (CRC Error)")
        else:
            print("x Підробку НЕ виявлено!")
    except:
         print("✓ Підробку виявлено (Critical Error)")

    print("\n[6] СПРОБА З НЕПРАВИЛЬНИМ КЛЮЧЕМ")
    print("-" * 40)
    
    fake_key = b'wrong_key_pattern'
    wrong_result = system.xor_cipher(extracted_data, fake_key)
    
    try:
        print(f"Результат: {wrong_result.decode('utf-8')}")
    except:
        print("✓ Без правильного ключа дані нечитабельні (символи сміття)")

if __name__ == "__main__":
    run_demo()