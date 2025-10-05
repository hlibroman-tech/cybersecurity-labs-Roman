import re
from datetime import datetime

def analyze_password_security():
    print("=" * 55)
    print("ПРОГРАМА АНАЛІЗУ БЕЗПЕКИ ПАРОЛІВ")
    print("=" * 55)
    
    # Введення даних
    password = input("Введіть пароль для аналізу: ")
    first_name = input("Введіть ім'я: ")
    last_name = input("Введіть прізвище (необов'язково): ")
    birth_date = input("Введіть дату народження (ДД.ММ.РРРР): ")
    
    print("=" * 55)
    print("АНАЛІЗ БЕЗПЕКИ ПАРОЛЯ")
    print("=" * 55)
    
    # Базова інформація
    print(f"Довжина: {len(password)} символів")
    print()
    
    # Аналіз персональних даних
    print("АНАЛІЗ ПЕРСОНАЛЬНИХ ДАНИХ:")
    personal_issues = []
    personal_score = 0
    
    # Перевірка імені
    if first_name and first_name.lower() in password.lower():
        personal_issues.append(f"- Містить ім'я '{first_name}'")
    
    # Перевірка прізвища
    if last_name and last_name.lower() in password.lower():
        personal_issues.append(f"- Містить прізвище '{last_name}'")
    
    # Перевірка дати народження
    if birth_date:
        date_parts = birth_date.split('.')
        if len(date_parts) == 3:
            day, month, year = date_parts
            
            # Перевірка року
            if year in password:
                personal_issues.append(f"- Містить рік народження '{year}'")
            
            # Перевірка дня
            if day in password:
                personal_issues.append(f"- Містить день народження '{day}'")
            
            # Перевірка місяця
            if month in password:
                personal_issues.append(f"- Містить місяць народження '{month}'")
    
    if personal_issues:
        for issue in personal_issues:
            print(issue)
        personal_score = max(0, 10 - len(personal_issues) * 3)
    else:
        print("- Не містить очевидних персональних даних ✓")
        personal_score = 10
    
    print(f"Оцінка за персональні дані: {personal_score}/10")
    print()
    
    # Аналіз складності
    print("АНАЛІЗ СКЛАДНОСТІ:")
    complexity_score = 0
    complexity_details = []
    
    # Довжина
    if len(password) >= 12:
        complexity_details.append(f"- Довжина >= 12 символів ✓ (+3)")
        complexity_score += 3
    else:
        complexity_details.append(f"- Довжина < 12 символів ✗")
    
    # Малі літери
    if re.search(r'[a-zа-яіїєґ]', password):
        complexity_details.append("- Містить малі літери ✓ (+1)")
        complexity_score += 1
    else:
        complexity_details.append("- Не містить малі літери ✗")
    
    # Великі літери
    if re.search(r'[A-ZА-ЯІЇЄҐ]', password):
        complexity_details.append("- Містить великі літери ✓ (+2)")
        complexity_score += 2
    else:
        complexity_details.append("- Не містить великих літер ✗")
    
    # Цифри
    if re.search(r'\d', password):
        complexity_details.append("- Містить цифри ✓ (+1)")
        complexity_score += 1
    else:
        complexity_details.append("- Не містить цифр ✗")
    
    # Спеціальні символи
    if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'"\\|,.<>/?]', password):
        complexity_details.append("- Містить спеціальні символи ✓ (+2)")
        complexity_score += 2
    else:
        complexity_details.append("- Не містить спеціальних символів ✗")
    
    # Різноманітність символів
    unique_chars = len(set(password))
    if unique_chars >= len(password) * 0.7:
        complexity_details.append(f"- Середня різноманітність символів ✓ (+1)")
        complexity_score += 1
    
    for detail in complexity_details:
        print(detail)
    
    print(f"Оцінка складності: {complexity_score}/10")
    print()
    
    # Загальна оцінка
    total_score = personal_score + complexity_score
    print("=" * 55)
    print(f"ЗАГАЛЬНА ОЦІНКА: {total_score}/20")
    
    # Рівень безпеки
    if total_score >= 17:
        security_level = "ВІДМІННИЙ"
    elif total_score >= 14:
        security_level = "ДОБРИЙ"
    elif total_score >= 10:
        security_level = "СЕРЕДНІЙ"
    elif total_score >= 6:
        security_level = "СЛАБКИЙ"
    else:
        security_level = "ДУЖЕ СЛАБКИЙ"
    
    print(f"РІВЕНЬ БЕЗПЕКИ: {security_level}")
    print("=" * 55)
    print()
    
    # Рекомендації
    print("РЕКОМЕНДАЦІЇ ДЛЯ ПОКРАЩЕННЯ:")
    recommendations = []
    
    if len(password) < 12:
        recommendations.append("- Збільште довжину паролю до мінімум 12 символів")
    
    if not re.search(r'[A-ZА-ЯІЇЄҐ]', password):
        recommendations.append("- Додайте великі літери")
    
    if not re.search(r'[a-zа-яіїєґ]', password):
        recommendations.append("- Додайте малі літери")
    
    if not re.search(r'\d', password):
        recommendations.append("- Додайте цифри")
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'"\\|,.<>/?]', password):
        recommendations.append("- Додайте спеціальні символи (!@#$%^&*)")
    
    if personal_issues:
        recommendations.append("- НЕ використовуйте персональні дані в паролі!")
    
    if not recommendations:
        recommendations.append("- Ваш пароль достатньо безпечний!")
        recommendations.append("- Не забувайте змінювати його регулярно")
    
    for rec in recommendations:
        print(rec)
    
    print("=" * 55)

# Запуск програми
if __name__ == "__main__":
    analyze_password_security()