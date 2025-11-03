import hashlib
import sys
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

print("--- Початок: Реалізація системи цифрових підписів ---")

print("\nБудь ласка, введіть ваші персональні дані для демонстрації.")
name = input("Введіть ім'я: ")
date_of_birth = input("Введіть дату народження (ДД.ММ.РРРР): ")
secret_word = input("Введіть секретне слово: ")
print("------------------------------------------------------")

print("1. Генерація пари ключів...")
personal_data_string = name + date_of_birth + secret_word
print(f"   Використовуємо дані: '{personal_data_string}' як основу.")

key_pair = RSA.generate(1024)
private_key = key_pair
public_key = key_pair.publickey()

print("   ...Справжню пару ключів RSA-1024 згенеровано.")
print(f"   Публічний ключ (початок): {public_key.export_key()[:50]}...")

print("\n2. Визначення функції створення підпису...")

def create_signature(document_content, priv_key):
    doc_hash = SHA256.new(document_content.encode('utf-8'))
    signer = pkcs1_15.new(priv_key)
    signature = signer.sign(doc_hash)
    return signature, doc_hash.hexdigest()

print("   ...Функцію 'create_signature' визначено.")

print("\n3. Визначення функції перевірки підпису...")

def verify_signature(document_content, signature, pub_key):
    doc_hash = SHA256.new(document_content.encode('utf-8'))
    verifier = pkcs1_15.new(pub_key)
    
    try:
        verifier.verify(doc_hash, signature)
        return True
    except (ValueError, TypeError):
        return False

print("   ...Функцію 'verify_signature' визначено.")

print("\n--- 4. ДЕМОНСТРАЦІЯ РОБОТИ ---")

original_document = "Це мій оригінальний документ. Він не повинен бути змінений."

print(f"\n[Крок А] Створення підпису для ОРИГІНАЛЬНОГО документа:")
print(f"   Текст: '{original_document}'")

original_signature, original_hash = create_signature(original_document, private_key)

print(f"   Хеш оригіналу: {original_hash}")
print(f"   Згенерований підпис (перші 16 байт): {original_signature[:16].hex()}...")

print(f"\n[Крок Б] Перевірка ОРИГІНАЛЬНОГО документа + ОРИГІНАЛЬНОГО підпису:")

is_valid = verify_signature(original_document, original_signature, public_key)

print(f"   Результат перевірки: {is_valid}")
if is_valid:
    print("   >>> ВЕРДИКТ: ПРАВДА. Підпис дійсний. Документ не змінено.")
else:
    print("   >>> ПОМИЛКА: Щось пішло не так.")

print(f"\n[Крок В] Демонстрація виявлення підробки (зміна в документі):")

tampered_document = "Це мій оригінальний документ. Він не повинен БУТИ змінений."
tampered_hash = SHA256.new(tampered_document.encode('utf-8')).hexdigest()

print(f"   Підроблений текст: '{tampered_document}'")
print(f"   Хеш підробки:   {tampered_hash}")
print(f"   Хеш оригіналу: {original_hash}")
print("   (Хеші не збігаються, оскільки текст змінено!)")

print(f"\n[Крок Г] Перевірка ПІДРОБЛЕНОГО документа + ОРИГІНАЛЬНОГО підпису:")

is_tampered_valid = verify_signature(tampered_document, original_signature, public_key)

print(f"   Результат перевірки: {is_tampered_valid}")
if not is_tampered_valid:
    print("   Система виявила підробку! Підпис не відповідає документу.")
else:
    print("   >>> ПОМИЛКА: Система не виявила підробку.")

print("\n--- Демонстрацію завершено ---")