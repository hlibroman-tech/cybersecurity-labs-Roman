import hashlib
import sys

print("Створення власної пари ключів")
name = "Гліб"
date_of_birth = "24.01.2005"
secret_word = "Заповіт"

print(f"\n1. Використання демонстраційних персональних даних:")
print(f"   - Ім'я: {name}")
print(f"   - Дата народження: {date_of_birth}")
print(f"   - Секретне слово: {secret_word}")

data_string = name + date_of_birth + secret_word

data_bytes = data_string.encode('utf-8')

private_key_hash = hashlib.sha256(data_bytes).hexdigest()

print(f"\n2. Згенеровано 'Приватний ключ' (SHA-256 хеш від даних):")
print(f"   {private_key_hash}")

public_key_hash = hashlib.sha256(private_key_hash.encode('utf-8')).hexdigest()

print(f"\n3. Згенеровано 'Публічний ключ' (SHA-256 хеш від приватного ключа):")
print(f"   {public_key_hash}")

#Зберегти ключі в окремих файлах.
try:
    with open("private.key", "w", encoding='utf-8') as f:
        f.write(private_key_hash)
        
    with open("public.key", "w", encoding='utf-8') as f:
        f.write(public_key_hash)
        
    print(f"\n4. Ключі успішно збережено в поточній директорії:")
    print(f"   - private.key")
    print(f"   - public.key")

except IOError as e:
    print(f"\n[ПОМИЛКА] Не вдалося зберегти файли: {e}", file=sys.stderr)

print("\n--- Завдання 'Крок 2' виконано ---")