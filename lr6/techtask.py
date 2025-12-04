import sqlite3

# --- НАЛАШТУВАННЯ БАЗИ ДАНИХ ---
def init_db():
    # Створюємо БД в оперативній пам'яті для тесту
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 1. Створення таблиці користувачів (students)
    cursor.execute('''
        CREATE TABLE students (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            grade REAL,
            password TEXT
        )
    ''')

    # 2. Створення таблиці з секретними даними (для демонстрації UNION атаки)
    cursor.execute('''
        CREATE TABLE secrets (
            id INTEGER PRIMARY KEY,
            secret_data TEXT
        )
    ''')

    # 3. Наповнення даними (ПЕРСОНАЛІЗОВАНО ДЛЯ РОМАН ГЛІБ)
    users_data = [
        (1, 'Роман Гліб', 'hlib.roman@hneu.net', 95.5, 'pass123'),  # Ваші дані
        (2, 'Іваненко Іван', 'ivanenko@hneu.net', 87.0, 'qwerty'),
        (3, 'Адміністратор', 'admin@hneu.net', 0.0, 'SuperSecretAdminPass')
    ]
    cursor.executemany('INSERT INTO students VALUES (?, ?, ?, ?, ?)', users_data)

    cursor.execute("INSERT INTO secrets VALUES (1, 'КЛЮЧ ДОСТУПУ: XYZ-999-SECRET')")
    
    conn.commit()
    return conn

# --- ВРАЗЛИВА ФУНКЦІЯ (Vulnerable) ---
def vulnerable_search(conn, search_query):
    cursor = conn.cursor()
    print("\n[ВРАЗЛИВА ВЕРСІЯ]")
    
    # ПОМИЛКА БЕЗПЕКИ: Пряма вставка змінної в рядок запиту (String Concatenation)
    sql = f"SELECT * FROM students WHERE name LIKE '{search_query}'"
    print(f"[SQL] {sql}") # Логування для звіту
    
    try:
        cursor.executescript(sql) 
        # Або звичайний execute для SELECT
        cursor.execute(sql)
        results = cursor.fetchall()
        
        if results:
            for row in results:
                print(f"  -> ID: {row[0]}, Ім'я: {row[1]}, Email: {row[2]}, Оцінка: {row[3]}")
            if len(results) > 1:
                print("  ! УВАГА: Отримано підозріло багато записів (ВИТІК ДАНИХ) !")
        else:
            print("  -> Результатів не знайдено")
    except Exception as e:
        print(f"  ! Помилка виконання SQL: {e}")

# --- ЗАХИЩЕНА ФУНКЦІЯ (Secure) ---
def secure_search(conn, search_query):
    cursor = conn.cursor()
    print("\n[ЗАХИЩЕНА ВЕРСІЯ]")
    
    # ЗАХИСТ: Використання плейсхолдера '?' (Parameterized Query)
    # SQL-код відокремлений від даних.
    sql = "SELECT * FROM students WHERE name LIKE ?"
    print(f"[SQL] {sql} з параметром ('{search_query}')")
    
    try:
        # Передаємо параметри окремим аргументом (кортежем)
        cursor.execute(sql, (search_query,))
        results = cursor.fetchall()
        
        if results:
            for row in results:
                print(f"  -> ID: {row[0]}, Ім'я: {row[1]}, Email: {row[2]}, Оцінка: {row[3]}")
        else:
            print("  -> Результатів не знайдено (Ін'єкція заблокована)")
    except Exception as e:
        print(f"  ! Помилка: {e}")

# --- ОСНОВНИЙ БЛОК ТЕСТУВАННЯ ---
if __name__ == "__main__":
    db_conn = init_db()
    
    print("="*60)
    print("ДЕМОНСТРАЦІЯ SQL-ІН'ЄКЦІЙ (Лабораторна робота №6)")
    print("Студент: Роман Гліб")
    print("="*60)

    # ТЕСТ 1: Нормальний пошук
    print("\n--- ТЕСТ 1: Звичайний пошук (легітимний запит) ---")
    user_input = "Роман Гліб" # Пошук по вашому імені
    vulnerable_search(db_conn, user_input)
    secure_search(db_conn, user_input)

    # ТЕСТ 2: Атака "OR 1=1" (Отримання всіх записів)
    print("\n--- ТЕСТ 2: SQL-ін'єкція ' OR '1'='1 (Витік даних) ---")
    attack_payload = "%' OR '1'='1" 
    print(f"Ввід користувача: {attack_payload}")
    
    vulnerable_search(db_conn, attack_payload)
    secure_search(db_conn, attack_payload)

    # ТЕСТ 3: UNION-атака (Доступ до секретної таблиці)
    print("\n--- ТЕСТ 3: UNION-атака (Крадіжка секретів) ---")
    # Підбираємо кількість колонок (тут 5 у students, тому додаємо null)
    union_payload = "%' UNION SELECT id, secret_data, NULL, NULL, NULL FROM secrets --"
    print(f"Ввід користувача: {union_payload}")
    
    vulnerable_search(db_conn, union_payload)
    secure_search(db_conn, union_payload)

    db_conn.close()