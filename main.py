import sqlite3

def create_connection(db_hw8):
    conn = None
    try:
        conn = sqlite3.connect(db_hw8)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(connection, sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except sqlite3.Error as e:
        print(e)

def insert_countries(connection, country):
    sql = '''INSERT INTO countries
    (titel)
    VALUES (?)'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (country,))
        connection.commit()
    except sqlite3.Error as e:
        print(e)

def insert_cities(connection, city):
    sql = '''INSERT INTO cities
    (titel, area, country_id)
    VALUES (?, ?, ?)'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, city)
        connection.commit()
    except sqlite3.Error as e:
        print(e)

def insert_employees(connection, employee):
    sql = '''INSERT INTO employees
    (first_name, last_name, city_id)
    VALUES (?, ?, ?)'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, employee)
        connection.commit()
    except sqlite3.Error as e:
        print(e)

sql_to_create_countries = '''
CREATE TABLE IF NOT EXISTS countries (
id INTEGER PRIMARY KEY AUTOINCREMENT,
titel VARCHAR (200) NOT NULL
)
'''

sql_to_create_cities = '''
CREATE TABLE IF NOT EXISTS cities (
id INTEGER PRIMARY KEY AUTOINCREMENT,
titel VARCHAR (200) NOT NULL,
area FLOAT (10, 2) NOT NULL DEFAULT 0.0,
country_id INTEGER,
FOREIGN KEY (country_id) REFERENCES countries(id)
)
'''

sql_to_create_employees = '''
CREATE TABLE IF NOT EXISTS employees (
id INTEGER PRIMARY KEY AUTOINCREMENT,
first_name VARCHAR (200) NOT NULL,
last_name VARCHAR (200) NOT NULL,
city_id INTEGER,
FOREIGN KEY (city_id) REFERENCES cities(id)
)
'''

def select_cities(connection):
    sql = "SELECT id, titel FROM cities"
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        cities = cursor.fetchall()
        return cities
    except sqlite3.Error as e:
        print(e)

def select_employees(connection, city_id):
    sql = '''SELECT employees.first_name, employees.last_name, countries.titel, cities.titel, cities.area
             FROM employees
             INNER JOIN cities ON employees.city_id = cities.id
             INNER JOIN countries ON cities.country_id = countries.id
             WHERE cities.id = ?'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (city_id,))
        employees = cursor.fetchall()
        return employees
    except sqlite3.Error as e:
        print(e)

def print_employees(employees):
    if len(employees) > 0:
        for employee in employees:
            first_name, last_name, country, city, area = employee
            print(f"Имя: {first_name}, Фамилия: {last_name}, Страна: {country}, Город: {city}, Площадь: {area}")
    else:
        print("Нет сотрудников в выбранном городе.")

db_file = "hw8.db"
connection = create_connection(db_file)

if connection is not None:
    print("Успешное подключение к базе данных!")

    create_table(connection, sql_to_create_countries)
    create_table(connection, sql_to_create_cities)
    create_table(connection, sql_to_create_employees)

    insert_countries(connection, 'Россия')
    insert_countries(connection, 'США')
    insert_countries(connection, 'Китай')

    insert_cities(connection, ('Москва', 25984.54, 1))
    insert_cities(connection, ('Питер', 5697.22, 1))
    insert_cities(connection, ('Хабаровск', 5879.14, 1))
    insert_cities(connection, ('Пекин', 69874.27, 3))
    insert_cities(connection, ('Гуанджоу', 51236.50, 3))
    insert_cities(connection, ('Нью-Йорк', 14879.44, 2))
    insert_cities(connection, ('Вашингтон', 58794.47, 2))

    insert_employees(connection, ('Андрей', 'Андреев', 1))
    insert_employees(connection, ('Петр', 'Петров', 1))
    insert_employees(connection, ('Сергей', 'Сергеев', 1))
    insert_employees(connection, ('Олег', 'Олегович', 2))
    insert_employees(connection, ('Антон', 'Антонов', 2))
    insert_employees(connection, ('Питре', 'Питресен', 2))
    insert_employees(connection, ('Джон', 'Джонсон', 3))
    insert_employees(connection, ('Смит', 'Смитрес', 3))
    insert_employees(connection, ('Андерс', 'Андерсон', 3))
    insert_employees(connection, ('Стив', 'Стивенс', 4))
    insert_employees(connection, ('Си', 'Дзин', 4))
    insert_employees(connection, ('Лю', 'Мэй', 4))
    insert_employees(connection, ('Лу', 'Мао', 5))
    insert_employees(connection, ('Хо', 'Гау', 5))
    insert_employees(connection, ('Мао', 'Ган', 5))

    while True:
        cities = select_cities(connection)

        print("\nВы можете отобразить список сотрудников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:")
        for city in cities:
            city_id, city_name = city
            print(f"ID: {city_id}, Город: {city_name}")

        city_id = input("\nВведите ID города: ")
        if city_id == "0":
            break

        employees = select_employees(connection, city_id)
        print_employees(employees)

    connection.close()