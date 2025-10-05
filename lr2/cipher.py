import string
from collections import Counter

class CaesarCipher:
    """Шифр Цезаря (зсув)"""
    
    def __init__(self, shift):
        self.shift = shift
        self.name = f"Цезар (зсув={shift})"
    
    def encrypt(self, text):
        """Шифрування тексту"""
        result = []
        for char in text:
            if char.isalpha():
                if char.isupper():
                    result.append(chr((ord(char) - ord('A') + self.shift) % 26 + ord('A')))
                else:
                    result.append(chr((ord(char) - ord('a') + self.shift) % 26 + ord('a')))
            else:
                result.append(char)
        return ''.join(result)
    
    def decrypt(self, text):
        """Розшифрування тексту"""
        self.shift = -self.shift
        decrypted = self.encrypt(text)
        self.shift = -self.shift
        return decrypted


class AffineCipher:
    """Шифр Афіна (ключ a, b)"""
    
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.name = f"Афін (a={a}, b={b})"
        self.m = 26
    
    def gcd(self, a, b):
        """Найбільший спільний дільник"""
        while b:
            a, b = b, a % b
        return a
    
    def mod_inverse(self, a, m):
        """Модульна обернена для a по модулю m"""
        for i in range(1, m):
            if (a * i) % m == 1:
                return i
        return None
    
    def encrypt(self, text):
        """Шифрування тексту"""
        if self.gcd(self.a, self.m) != 1:
            raise ValueError(f"Ключ a={self.a} не є взаємно простим з {self.m}")
        
        result = []
        for char in text:
            if char.isalpha():
                if char.isupper():
                    x = ord(char) - ord('A')
                    encrypted = (self.a * x + self.b) % self.m
                    result.append(chr(encrypted + ord('A')))
                else:
                    x = ord(char) - ord('a')
                    encrypted = (self.a * x + self.b) % self.m
                    result.append(chr(encrypted + ord('a')))
            else:
                result.append(char)
        return ''.join(result)
    
    def decrypt(self, text):
        """Розшифрування тексту"""
        if self.gcd(self.a, self.m) != 1:
            raise ValueError(f"Ключ a={self.a} не є взаємно простим з {self.m}")
        
        a_inv = self.mod_inverse(self.a, self.m)
        if a_inv is None:
            raise ValueError(f"Не існує оберненого для a={self.a}")
        
        result = []
        for char in text:
            if char.isalpha():
                if char.isupper():
                    y = ord(char) - ord('A')
                    decrypted = (a_inv * (y - self.b)) % self.m
                    result.append(chr(decrypted + ord('A')))
                else:
                    y = ord(char) - ord('a')
                    decrypted = (a_inv * (y - self.b)) % self.m
                    result.append(chr(decrypted + ord('a')))
            else:
                result.append(char)
        return ''.join(result)


def generate_keys_from_initials(name="Роман", surname="Гліб"):
    """Генерація ключів на основі ініціалів"""
    print("ГЕНЕРАЦІЯ КЛЮЧІВ НА ОСНОВІ ПЕРСОНАЛЬНИХ ДАНИХ:")
    print("="*70)
    print(f"Ініціали: {name} {surname}")
    print()
    
    # Ключ для Цезаря
    first_letter = name[0].upper()
    if ord(first_letter) >= ord('А') and ord(first_letter) <= ord('Я'):
        # Кирилиця
        caesar_key = (ord(first_letter) - ord('А') + 1) % 26
    else:
        # Латиниця
        caesar_key = ord(first_letter) - ord('A') + 1
    
    caesar_key = max(1, caesar_key % 26)
    print(f"Шифр Цезаря:")
    print(f"  Перша літера імені '{name[0]}' -> позиція {caesar_key}")
    print(f"  Згенерований ключ: зсув = {caesar_key}")
    print()
    
    # Ключі для Афіна
    valid_a = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    
    first_letter_name = name[0].upper()
    first_letter_surname = surname[0].upper()
    
    # Розраховуємо a на основі імені
    if ord(first_letter_name) >= ord('А') and ord(first_letter_name) <= ord('Я'):
        name_pos = (ord(first_letter_name) - ord('А') + 1) % 26
    else:
        name_pos = ord(first_letter_name) - ord('A') + 1
    a = valid_a[name_pos % len(valid_a)]
    
    # Розраховуємо b на основі прізвища
    if ord(first_letter_surname) >= ord('А') and ord(first_letter_surname) <= ord('Я'):
        surname_pos = (ord(first_letter_surname) - ord('А') + 1) % 26
    else:
        surname_pos = ord(first_letter_surname) - ord('A') + 1
    b = surname_pos % 26
    
    print(f"Шифр Афіна:")
    print(f"  Перша літера імені '{name[0]}' -> a = {a}")
    print(f"  Перша літера прізвища '{surname[0]}' -> b = {b}")
    print(f"  Згенеровані ключі: a = {a}, b = {b}")
    
    return caesar_key, a, b


class CipherAnalyzer:
    """Аналіз та порівняння шифрів"""
    
    def __init__(self):
        self.results = []
    
    def analyze_cipher(self, cipher, plaintext):
        """Аналіз одного шифру"""
        print(f"\n{'='*70}")
        print(f"Аналіз шифру: {cipher.name}")
        print(f"{'='*70}")
        
        # Шифрування
        encrypted = cipher.encrypt(plaintext)
        print(f"\nВихідний текст: {plaintext}")
        print(f"Зашифрований:   {encrypted}")
        
        # Розшифрування
        decrypted = cipher.decrypt(encrypted)
        print(f"Розшифрований:  {decrypted}")
        
        # Перевірка коректності
        success = plaintext == decrypted
        print(f"\nПеревірка: {'✓ Успішно' if success else '✗ Помилка'}")
        
        # Статистика
        stats = self.calculate_statistics(plaintext, encrypted)
        
        self.results.append({
            'cipher': cipher.name,
            'plaintext': plaintext,
            'encrypted': encrypted,
            'decrypted': decrypted,
            'success': success,
            'stats': stats
        })
        
        return stats
    
    def calculate_statistics(self, plaintext, encrypted):
        """Розрахунок статистичних характеристик"""
        # Частота букв
        plain_freq = Counter(c.upper() for c in plaintext if c.isalpha())
        encrypted_freq = Counter(c.upper() for c in encrypted if c.isalpha())
        
        # Довжина
        length = len([c for c in plaintext if c.isalpha()])
        
        # Унікальні символи
        unique_plain = len(plain_freq)
        unique_encrypted = len(encrypted_freq)
        
        stats = {
            'length': length,
            'unique_plain': unique_plain,
            'unique_encrypted': unique_encrypted,
            'plain_freq': plain_freq,
            'encrypted_freq': encrypted_freq
        }
        
        print(f"\nСтатистика:")
        print(f"  Довжина тексту: {length} літер")
        print(f"  Унікальних символів (відкритий текст): {unique_plain}")
        print(f"  Унікальних символів (зашифрований): {unique_encrypted}")
        
        return stats
    
    def compare_ciphers(self):
        """Порівняльний аналіз всіх шифрів"""
        print(f"\n{'='*70}")
        print("ПОРІВНЯЛЬНИЙ АНАЛІЗ ШИФРІВ")
        print(f"{'='*70}")
        
        print(f"\n{'Метод':<30} {'Довжина':<10} {'Унік.симв.':<12} {'Результат'}")
        print("-" * 70)
        
        for result in self.results:
            print(f"{result['cipher']:<30} "
                  f"{result['stats']['length']:<10} "
                  f"{result['stats']['unique_encrypted']:<12} "
                  f"{'✓' if result['success'] else '✗'}")
        
        # Таблиця частот (топ-5 для кожного методу)
        print(f"\n{'='*70}")
        print("ТОП-5 НАЙЧАСТІШИХ БУКВ")
        print(f"{'='*70}")
        
        for result in self.results:
            print(f"\n{result['cipher']}:")
            print("  Відкритий текст:", 
                  ', '.join([f"{k}:{v}" for k, v in result['stats']['plain_freq'].most_common(5)]))
            print("  Зашифрований:   ", 
                  ', '.join([f"{k}:{v}" for k, v in result['stats']['encrypted_freq'].most_common(5)]))


# Демонстрація роботи
def main():
    print("ПРОГРАМА: ПОРІВНЯЛЬНИЙ АНАЛІЗ ШИФРІВ")
    print("="*70)
    print()
    
    # Персональні дані
    name = "Роман"
    surname = "Гліб"
    
    # Тестовий текст
    test_text = "Zahist informacii - vazhliva disciplina"
    
    # Генерація ключів на основі ініціалів
    caesar_key, affine_a, affine_b = generate_keys_from_initials(name, surname)
    
    # Створення шифрів
    caesar = CaesarCipher(shift=caesar_key)
    affine = AffineCipher(a=affine_a, b=affine_b)
    
    # Створення аналізатора
    analyzer = CipherAnalyzer()
    
    # Аналіз кожного шифру
    analyzer.analyze_cipher(caesar, test_text)
    analyzer.analyze_cipher(affine, test_text)
    
    # Порівняльний аналіз
    analyzer.compare_ciphers()
    
    # Висновки про стійкість
    print(f"\n{'='*70}")
    print("ВИСНОВКИ ПРО СТІЙКІСТЬ КОЖНОГО МЕТОДУ")
    print(f"{'='*70}")
    print("\nШифр Цезаря:")
    print("  + Простота реалізації та використання")
    print("  - Низька криптостійкість (лише 25 можливих ключів)")
    print("  - Легко зламати методом перебору")
    print("  - Вразливий до частотного аналізу")
    
    print("\nШифр Афіна:")
    print("  + Складніший за Цезаря (більше можливих ключів)")
    print("  + Використовує множення та додавання")
    print("  - Також вразливий до частотного аналізу")
    print("  - Обмежена кількість можливих ключів (~312)")
    print("  - Ключ 'a' повинен бути взаємно простим з 26")
    print("="*70)


if __name__ == "__main__":
    main()