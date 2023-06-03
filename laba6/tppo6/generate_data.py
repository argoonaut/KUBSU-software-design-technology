import sqlite3
from faker import Faker

fake = Faker()

# Подключение к базе данных
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Количество записей для каждой таблицы
num_records = 5000

# Генерация данных для таблицы Courses
for _ in range(num_records):
    name = fake.sentence()
    price = fake.random_number(digits=5)
    description = fake.text()
    is_ready = fake.boolean()

    cursor.execute(
        "INSERT INTO Courses (Name, Price, Description, IsReady) VALUES (?, ?, ?, ?)",
        (name, price, description, is_ready)
    )

# Генерация данных для таблицы Instructors
for _ in range(num_records):
    first_name = fake.first_name()
    last_name = fake.last_name()
    middle_name = fake.first_name()
    course_id = fake.random_int(min=1, max=num_records)

    cursor.execute(
        "INSERT INTO Instructors (FirstName, LastName, MiddleName, CourseID) VALUES (?, ?, ?, ?)",
        (first_name, last_name, middle_name, course_id)
    )

# Генерация данных для таблицы Cashiers
for _ in range(num_records):
    first_name = fake.first_name()
    last_name = fake.last_name()
    middle_name = fake.first_name()
    machine_id = fake.random_number(digits=5)

    cursor.execute(
        "INSERT INTO Cashiers (FirstName, LastName, MiddleName, MachineID) VALUES (?, ?, ?, ?)",
        (first_name, last_name, middle_name, machine_id)
    )

# Генерация данных для таблицы Clients
for _ in range(num_records):
    first_name = fake.first_name()
    last_name = fake.last_name()
    phone_number = fake.phone_number()
    email = fake.email()

    cursor.execute(
        "INSERT INTO Clients (FirstName, LastName, PhoneNumber, Email) VALUES (?, ?, ?, ?)",
        (first_name, last_name, phone_number, email)
    )

# Запись данных в базу данных
conn.commit()
conn.close()

print(f"{num_records} записей было добавлено в каждую таблицу.")
