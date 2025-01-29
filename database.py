import sqlite3
from hashlib import sha256

def init_db():
    conn = sqlite3.connect('sport_inventory.db')
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,  # Добавлено поле email
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
        )
    ''')

    # Таблица инвентаря
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('new', 'used', 'broken'))
        )
    ''')

    # Таблица заявок
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('pending', 'approved', 'rejected', 'repair')),
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(item_id) REFERENCES inventory(id)
        )
    ''')

    # Таблица закупок
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            supplier TEXT NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY(item_id) REFERENCES inventory(id)
        )
    ''')

    # Создаем тестового администратора, если его нет
    cursor.execute('SELECT * FROM users WHERE username = "admin"')
    if not cursor.fetchone():
        hashed_password = sha256("admin123".encode()).hexdigest()  # Пароль: admin123
        cursor.execute('INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)', 
                       ("admin", "admin@example.com", hashed_password, "admin"))

    conn.commit()
    conn.close()

def execute_query(query, params=()):
    conn = sqlite3.connect('sport_inventory.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def fetch_query(query, params=()):
    conn = sqlite3.connect('sport_inventory.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

def hash_password(password):
    """Хеширует пароль с использованием SHA-256."""
    return sha256(password.encode()).hexdigest()

def create_user(username, email, password, role):
    """Создает нового пользователя, если его имя и email уникальны."""
    # Проверяем, существует ли пользователь с таким именем или email
    existing_user = fetch_query('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
    if existing_user:
        print("Ошибка: Пользователь с таким именем или email уже существует.")
        return False  # Возвращаем False, если пользователь уже существует

    # Если пользователь не существует, создаем его
    hashed_password = hash_password(password)
    execute_query('INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)', 
                  (username, email, hashed_password, role))
    print("Пользователь успешно зарегистрирован!")
    return True  # Возвращаем True, если регистрация прошла успешно

def authenticate_user(email, password):
    """Проверяет, существует ли пользователь с таким email и паролем."""
    hashed_password = hash_password(password)
    return fetch_query('SELECT * FROM users WHERE email = ? AND password = ?', (email, hashed_password))

def clear_users_table():
    """Очищает таблицу users."""
    execute_query('DELETE FROM users')
    print("Таблица users очищена.")