import sqlite3


# Функция для инициализации базы данных и создания таблицы Products
def initiate_db():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()

    # Создание таблицы Products
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# Функция для получения всех продуктов из таблицы
def get_all_products():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()

    # Получение всех записей из таблицы Products
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()

    connection.close()
    return products


# Функция для добавления записей в таблицу (пополнения базы)
def add_product(title, description, price):
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()

    # Вставка новой записи
    cursor.execute("""
        INSERT INTO Products (title, description, price)
        VALUES (?, ?, ?)
    """, (title, description, price))

    connection.commit()
    connection.close()
