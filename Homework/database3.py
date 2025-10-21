import sqlite3
from datetime import date

def create_database():
    """Создание базы данных и таблиц"""
    conn = sqlite3.connect('academy.db')
    cursor = conn.cursor()

    # Создание таблицы Кафедры (Departments)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Departments (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Financing REAL NOT NULL DEFAULT 0 CHECK (Financing >= 0),
            Name TEXT NOT NULL UNIQUE CHECK (Name != '')
        )
    ''')

    # Создание таблицы Факультеты (Faculties)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Faculties (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Dean TEXT NOT NULL CHECK (Dean != ''),
            Name TEXT NOT NULL UNIQUE CHECK (Name != '')
        )
    ''')

    # Создание таблицы Группы (Groups)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Groups (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL UNIQUE CHECK (Name != ''),
            Rating INTEGER NOT NULL CHECK (Rating >= 0 AND Rating <= 5),
            Year INTEGER NOT NULL CHECK (Year >= 1 AND Year <= 5)
        )
    ''')

    # Создание таблицы Преподаватели (Teachers)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Teachers (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            EmploymentDate DATE NOT NULL CHECK (EmploymentDate >= '1990-01-01'),
            IsAssistant INTEGER NOT NULL DEFAULT 0,
            IsProfessor INTEGER NOT NULL DEFAULT 0,
            Name TEXT NOT NULL CHECK (Name != ''),
            Position TEXT NOT NULL CHECK (Position != ''),
            Premium REAL NOT NULL DEFAULT 0 CHECK (Premium >= 0),
            Salary REAL NOT NULL CHECK (Salary > 0),
            Surname TEXT NOT NULL CHECK (Surname != '')
        )
    ''')

    # Заполнение таблиц тестовыми данными
    insert_test_data(cursor)

    conn.commit()
    conn.close()
    print("База данных 'Академия' успешно создана и заполнена тестовыми данными!")


def insert_test_data(cursor):
    """Заполнение таблиц тестовыми данными"""

    # Добавление кафедр
    departments = [
        (12000, 'Software Development'),
        (15000, 'Computer Science'),
        (8000, 'Mathematics'),
        (30000, 'Physics'),
        (9000, 'Foreign Languages')
    ]
    cursor.executemany('INSERT INTO Departments (Financing, Name) VALUES (?, ?)', departments)

    # Добавление факультетов
    faculties = [
        ('Dr. Smith', 'Computer Science'),
        ('Dr. Johnson', 'Engineering'),
        ('Dr. Brown', 'Mathematics'),
        ('Dr. Wilson', 'Physics')
    ]
    cursor.executemany('INSERT INTO Faculties (Dean, Name) VALUES (?, ?)', faculties)

    # Добавление групп
    groups = [
        ('CS-101', 4, 1),
        ('CS-201', 3, 2),
        ('ENG-101', 5, 1),
        ('MATH-301', 2, 3),
        ('PHYS-501', 4, 5),
        ('CS-301', 3, 3)
    ]
    cursor.executemany('INSERT INTO Groups (Name, Rating, Year) VALUES (?, ?, ?)', groups)

    # Добавление преподавателей
    teachers = [
        ('2000-01-15', 0, 1, 'John', 'Professor', 500, 2000, 'Smith'),
        ('1999-05-20', 1, 0, 'Alice', 'Assistant', 200, 800, 'Johnson'),
        ('2005-08-10', 0, 1, 'Robert', 'Professor', 600, 1200, 'Brown'),
        ('1998-03-01', 1, 0, 'Emily', 'Assistant', 550, 500, 'Davis'),
        ('2002-11-15', 1, 0, 'Michael', 'Assistant', 160, 600, 'Wilson'),
        ('1995-09-01', 0, 0, 'Sarah', 'Senior Lecturer', 300, 900, 'Taylor'),
        ('1999-12-10', 1, 0, 'David', 'Assistant', 100, 400, 'Clark'),
        ('2001-06-20', 0, 1, 'Jennifer', 'Professor', 700, 1500, 'White')
    ]
    cursor.executemany('''
        INSERT INTO Teachers (EmploymentDate, IsAssistant, IsProfessor, Name, Position, Premium, Salary, Surname) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', teachers)

    print("Тестовые данные успешно добавлены!")


def execute_queries():
    """Выполнение всех запросов"""
    conn = sqlite3.connect('academy.db')
    cursor = conn.cursor()

    print("\n" + "=" * 80)
    print("ЗАПРОСЫ К БАЗЕ ДАННЫХ 'АКАДЕМИЯ'")
    print("=" * 80)

    # Запрос 1: Вывести таблицу кафедр в обратном порядке полей
    print("\n1. Таблица кафедр (поля в обратном порядке):")
    cursor.execute('SELECT Name, Financing, Id FROM Departments')
    results = cursor.fetchall()
    for row in results:
        print(f"Название: {row[0]}, Финансирование: {row[1]}, ID: {row[2]}")

    # Запрос 2: Вывести названия групп и их рейтинги с уточнением имен полей
    print("\n2. Названия групп и их рейтинги:")
    cursor.execute('SELECT Groups.Name as "Group Name", Groups.Rating as "Group Rating" FROM Groups')
    results = cursor.fetchall()
    for row in results:
        print(f"Группа: {row[0]}, Рейтинг: {row[1]}")

    # Запрос 3: Процент ставки по отношению к надбавке и зарплате
    print("\n3. Фамилии преподавателей и проценты ставки:")
    cursor.execute('''
        SELECT Surname, 
               ROUND((Salary * 100.0 / CASE WHEN Premium = 0 THEN 1 ELSE Premium END), 2) as SalaryToPremiumPercent,
               ROUND((Salary * 100.0 / (Salary + Premium)), 2) as SalaryToTotalPercent
        FROM Teachers
    ''')
    results = cursor.fetchall()
    for row in results:
        print(f"Фамилия: {row[0]}, Ставка/Надбавка: {row[1]}%, Ставка/Зарплата: {row[2]}%")

    # Запрос 4: Таблица факультетов в специальном формате
    print("\n4. Факультеты в формате 'The dean of faculty...':")
    cursor.execute('SELECT Name, Dean FROM Faculties')
    results = cursor.fetchall()
    for row in results:
        print(f"The dean of faculty {row[0]} is {row[1]}.")

    # Запрос 5: Профессоры со ставкой > 1050
    print("\n5. Профессоры со ставкой > 1050:")
    cursor.execute('SELECT Surname FROM Teachers WHERE IsProfessor = 1 AND Salary > 1050')
    results = cursor.fetchall()
    for row in results:
        print(f"Фамилия: {row[0]}")

    # Запрос 6: Кафедры с финансированием < 11000 или > 25000
    print("\n6. Кафедры с финансированием < 11000 или > 25000:")
    cursor.execute('SELECT Name FROM Departments WHERE Financing < 11000 OR Financing > 25000')
    results = cursor.fetchall()
    for row in results:
        print(f"Кафедра: {row[0]}")

    # Запрос 7: Факультеты кроме Computer Science
    print("\n7. Факультеты кроме 'Computer Science':")
    cursor.execute('SELECT Name FROM Faculties WHERE Name != "Computer Science"')
    results = cursor.fetchall()
    for row in results:
        print(f"Факультет: {row[0]}")

    # Запрос 8: Преподаватели не профессоры
    print("\n8. Преподаватели не профессоры:")
    cursor.execute('SELECT Surname, Position FROM Teachers WHERE IsProfessor = 0')
    results = cursor.fetchall()
    for row in results:
        print(f"Фамилия: {row[0]}, Должность: {row[1]}")

    # Запрос 9: Ассистенты с надбавкой от 160 до 550
    print("\n9. Ассистенты с надбавкой от 160 до 550:")
    cursor.execute('''
        SELECT Surname, Position, Salary, Premium 
        FROM Teachers 
        WHERE IsAssistant = 1 AND Premium BETWEEN 160 AND 550
    ''')
    results = cursor.fetchall()
    for row in results:
        print(f"Фамилия: {row[0]}, Должность: {row[1]}, Ставка: {row[2]}, Надбавка: {row[3]}")

    # Запрос 10: Фамилии и ставки ассистентов
    print("\n10. Фамилии и ставки ассистентов:")
    cursor.execute('SELECT Surname, Salary FROM Teachers WHERE IsAssistant = 1')
    results = cursor.fetchall()
    for row in results:
        print(f"Фамилия: {row[0]}, Ставка: {row[1]}")

    # Запрос 11: Преподаватели принятые до 01.01.2000
    print("\n11. Преподаватели принятые до 01.01.2000:")
    cursor.execute('SELECT Surname, Position FROM Teachers WHERE EmploymentDate < "2000-01-01"')
    results = cursor.fetchall()
    for row in results:
        print(f"Фамилия: {row[0]}, Должность: {row[1]}")

    # Запрос 12: Кафедры до Software Development в алфавитном порядке
    print("\n12. Кафедры до 'Software Development' в алфавитном порядке:")
    cursor.execute('''
        SELECT Name as "Name of Department" 
        FROM Departments 
        WHERE Name < "Software Development" 
        ORDER BY Name
    ''')
    results = cursor.fetchall()
    for row in results:
        print(f"Кафедра: {row[0]}")

    # Запрос 13: Ассистенты с зарплатой <= 1200
    print("\n13. Ассистенты с зарплатой <= 1200:")
    cursor.execute('SELECT Surname FROM Teachers WHERE IsAssistant = 1 AND (Salary + Premium) <= 1200')
    results = cursor.fetchall()
    for row in results:
        print(f"Фамилия: {row[0]}")

    # Запрос 14: Группы 5-го курса с рейтингом 2-4
    print("\n14. Группы 5-го курса с рейтингом 2-4:")
    cursor.execute('SELECT Name FROM Groups WHERE Year = 5 AND Rating BETWEEN 2 AND 4')
    results = cursor.fetchall()
    for row in results:
        print(f"Группа: {row[0]}")

    # Запрос 15: Ассистенты со ставкой < 550 или надбавкой < 200
    print("\n15. Ассистенты со ставкой < 550 или надбавкой < 200:")
    cursor.execute('SELECT Surname FROM Teachers WHERE IsAssistant = 1 AND (Salary < 550 OR Premium < 200)')
    results = cursor.fetchall()
    for row in results:
        print(f"Фамилия: {row[0]}")

    conn.close()


def main():
    """Основная функция"""
    try:
        # Создание базы данных
        create_database()

        # Выполнение запросов
        execute_queries()

        print("\n" + "=" * 80)
        print("Все операции успешно завершены!")
        print("=" * 80)

    except sqlite3.Error as e:
        print(f"Ошибка SQLite: {e}")
    except Exception as e:
        print(f"Общая ошибка: {e}")


if __name__ == "__main__":
    main()