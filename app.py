from database import init_db, clear_users_table
from admin import admin_login
from user import user_register, user_login

# Инициализация базы данных (создание таблиц, если их нет)
init_db()

# Очистка таблицы users (для тестирования, опционально)
# clear_users_table()

def main_menu():
    while True:
        print("\n1. Войти как администратор")
        print("2. Зарегистрироваться как пользователь")
        print("3. Войти как пользователь")
        print("4. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            admin_login()
        elif choice == '2':
            user_register()
        elif choice == '3':
            user_login()
        elif choice == '4':
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main_menu()