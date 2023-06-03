import sqlite3

def connect_to_db():
    connection = sqlite3.connect("database.db")
    return connection

def create_tables(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS Courses (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name TEXT NOT NULL,
                        Price REAL NOT NULL,
                        Description TEXT,
                        IsReady BOOLEAN NOT NULL
                    );""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS Instructors (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        FirstName TEXT NOT NULL,
                        LastName TEXT NOT NULL,
                        MiddleName TEXT,
                        CourseID INTEGER,
                        FOREIGN KEY (CourseID) REFERENCES Courses (ID)
                    );""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS Cashiers (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        FirstName TEXT NOT NULL,
                        LastName TEXT NOT NULL,
                        MiddleName TEXT,
                        MachineID INTEGER NOT NULL
                    );""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS Clients (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        FirstName TEXT NOT NULL,
                        LastName TEXT NOT NULL,
                        PhoneNumber TEXT NOT NULL,
                        Email TEXT NOT NULL
                    );""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS Sales (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        CourseID INTEGER,
                        CashierID INTEGER,
                        ClientID INTEGER,
                        FOREIGN KEY (CourseID) REFERENCES Courses (ID),
                        FOREIGN KEY (CashierID) REFERENCES Cashiers (ID),
                        FOREIGN KEY (ClientID) REFERENCES Clients (ID)
                    );""")
