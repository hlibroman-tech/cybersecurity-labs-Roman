import sqlite3

def setup_database():
    """Створюємо тестову базу даних у пам'яті та наповнюємо її даними."""
    conn = sqlite3.connect(':memory:')  # БД живе лише під час роботи скрипта
    cursor = conn.cursor()
    
    # Створення таблиці
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            is_admin INTEGER
        )
    ''')
    
    # Додавання тестових даних (як на скріншоті)
    users = [
        ('administrator', 'super_secret_pass', 1),
        ('ivan_student', 'student_pass', 0),
        ('guest', 'guest', 0)
    ]
    
    cursor.executemany('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', users)
    conn.commit()
    return conn

def vulnerable_search(conn, payload):
    """Вразлива функція: використовує пряму конкатенацію (f-strings)."""
    cursor = conn.cursor()
    
    print("\n========== [TEST 1] Вразлива версія (Vulnerable) ==========")
    print(f"Введений Payload: {payload}")
    
    # НЕБЕЗПЕЧНО: Пряма вставка даних у запит
    sql_query = f"SELECT * FROM users WHERE username = '{payload}'"
    
    print(f"[LOG] Виконується SQL: {sql_query}")
    
    try:
        # cursor.executescript() дозволяє виконати декілька команд, що часто використовується при ін'єкціях,
        # але тут достатньо execute для демонстрації WHERE-ін'єкції.
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        if results:
            print(f"[RESULT] УВАГА! Витік даних ({len(results)} записів):")
            for row in results:
                print(f" -> {row}")
        else:
            print("[RESULT] Нічого не знайдено.")
            
    except sqlite3.Error as e:
        print(f"[ERROR] Помилка SQL: {e}")

def secure_search(conn, payload):
    """Захищена функція: використовує параметризовані запити."""
    cursor = conn.cursor()
    
    print("\n========== [TEST 2] Захищена версія (Fixed) ==========")
    print(f"Введений Payload: {payload}")
    
    # БЕЗПЕЧНО: Використання знака ? як плейсхолдера
    sql_query = "SELECT * FROM users WHERE username = ?"
    
    print(f"[LOG] Виконується SQL: {sql_query} з параметром ('{payload}')")
    
    try:
        # Дані передаються окремим аргументом (кортежем)
        cursor.execute(sql_query, (payload,))
        results = cursor.fetchall()
        
        if results:
            print(f"[RESULT] Знайдено: {results}")
        else:
            print("[RESULT] Нічого не знайдено (Атака успішно заблокована).")
            
    except sqlite3.Error as e:
        print(f"[ERROR] Помилка SQL: {e}")

# === ГОЛОВНА ЧАСТИНА ПРОГРАМИ ===
if __name__ == "__main__":
    # 1. Підготовка БД
    connection = setup_database()
    
    # 2. Визначаємо шкідливий ввід (Payload)
    # Цей пейлоад робить умову завжди істинною: ' (закриває лапку) OR '1'='1
    malicious_input = "' OR '1'='1"
    
    # 3. Запуск тестів
    vulnerable_search(connection, malicious_input)
    secure_search(connection, malicious_input)
    
    # 4. Закриття з'єднання
    connection.close()