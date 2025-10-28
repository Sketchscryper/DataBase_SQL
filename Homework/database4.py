import sqlite3

def create_database():
    """Создание базы данных и таблиц"""
    conn = sqlite3.connect('academy.db')
    cursor = conn.cursor()

    # Создание таблиц
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS Faculties (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Financing REAL NOT NULL DEFAULT 0 CHECK (Financing >= 0),
            Name TEXT NOT NULL UNIQUE CHECK (Name != '')
        );

        CREATE TABLE IF NOT EXISTS Departments (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Financing REAL NOT NULL DEFAULT 0 CHECK (Financing >= 0),
            Name TEXT NOT NULL UNIQUE CHECK (Name != ''),
            FacultyId INTEGER NOT NULL,
            FOREIGN KEY (FacultyId) REFERENCES Faculties(Id)
        );

        CREATE TABLE IF NOT EXISTS Curators (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL CHECK (Name != ''),
            Surname TEXT NOT NULL CHECK (Surname != '')
        );

        CREATE TABLE IF NOT EXISTS Groups (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL UNIQUE CHECK (Name != ''),
            Year INTEGER NOT NULL CHECK (Year BETWEEN 1 AND 5),
            DepartmentId INTEGER NOT NULL,
            FOREIGN KEY (DepartmentId) REFERENCES Departments(Id)
        );

        CREATE TABLE IF NOT EXISTS GroupsCurators (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            CuratorId INTEGER NOT NULL,
            GroupId INTEGER NOT NULL,
            FOREIGN KEY (CuratorId) REFERENCES Curators(Id),
            FOREIGN KEY (GroupId) REFERENCES Groups(Id)
        );

        CREATE TABLE IF NOT EXISTS Teachers (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL CHECK (Name != ''),
            Salary REAL NOT NULL CHECK (Salary > 0),
            Surname TEXT NOT NULL CHECK (Surname != '')
        );

        CREATE TABLE IF NOT EXISTS Subjects (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL UNIQUE CHECK (Name != '')
        );

        CREATE TABLE IF NOT EXISTS Lectures (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            LectureRoom TEXT NOT NULL CHECK (LectureRoom != ''),
            SubjectId INTEGER NOT NULL,
            TeacherId INTEGER NOT NULL,
            FOREIGN KEY (SubjectId) REFERENCES Subjects(Id),
            FOREIGN KEY (TeacherId) REFERENCES Teachers(Id)
        );

        CREATE TABLE IF NOT EXISTS GroupsLectures (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            GroupId INTEGER NOT NULL,
            LectureId INTEGER NOT NULL,
            FOREIGN KEY (GroupId) REFERENCES Groups(Id),
            FOREIGN KEY (LectureId) REFERENCES Lectures(Id)
        );
    ''')

    # Вставка тестовых данных
    insert_test_data(cursor)

    conn.commit()
    return conn


def insert_test_data(cursor):
    """Вставка тестовых данных"""
    # Факультеты
    faculties = [
        (100000, 'Computer Science'),
        (80000, 'Mathematics'),
        (90000, 'Physics')
    ]
    cursor.executemany('INSERT INTO Faculties (Financing, Name) VALUES (?, ?)', faculties)

    # Кафедры
    departments = [
        (50000, 'Software Engineering', 1),
        (60000, 'Data Science', 1),
        (40000, 'Algebra', 2),
        (45000, 'Mathematical Analysis', 2),
        (40000, 'Quantum Physics', 3)
    ]
    cursor.executemany('INSERT INTO Departments (Financing, Name, FacultyId) VALUES (?, ?, ?)', departments)

    # Кураторы
    curators = [
        ('John', 'Smith'),
        ('Emily', 'Johnson'),
        ('Michael', 'Brown'),
        ('Sarah', 'Davis')
    ]
    cursor.executemany('INSERT INTO Curators (Name, Surname) VALUES (?, ?)', curators)

    # Группы
    groups = [
        ('P107', 1, 1),
        ('P108', 2, 1),
        ('M201', 3, 3),
        ('M202', 4, 4),
        ('P501', 5, 2),
        ('P502', 5, 2)
    ]
    cursor.executemany('INSERT INTO Groups (Name, Year, DepartmentId) VALUES (?, ?, ?)', groups)

    # Преподаватели
    teachers = [
        ('Samantha', 50000, 'Adams'),
        ('Robert', 45000, 'Wilson'),
        ('Jennifer', 48000, 'Miller'),
        ('David', 52000, 'Taylor')
    ]
    cursor.executemany('INSERT INTO Teachers (Name, Salary, Surname) VALUES (?, ?, ?)', teachers)

    # Дисциплины
    subjects = [
        ('Database Theory',),
        ('Algorithms',),
        ('Linear Algebra',),
        ('Quantum Mechanics',)
    ]
    cursor.executemany('INSERT INTO Subjects (Name) VALUES (?)', subjects)

    # Лекции
    lectures = [
        ('B103', 1, 1),
        ('A205', 2, 2),
        ('B103', 1, 3),
        ('C301', 3, 4),
        ('B103', 4, 1)
    ]
    cursor.executemany('INSERT INTO Lectures (LectureRoom, SubjectId, TeacherId) VALUES (?, ?, ?)', lectures)

    # Связи групп и кураторов
    groups_curators = [
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 4),
        (6, 4)
    ]
    cursor.executemany('INSERT INTO GroupsCurators (CuratorId, GroupId) VALUES (?, ?)', groups_curators)

    # Связи групп и лекций
    groups_lectures = [
        (1, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (5, 5),
        (6, 5)
    ]
    cursor.executemany('INSERT INTO GroupsLectures (GroupId, LectureId) VALUES (?, ?)', groups_lectures)


def execute_queries(conn):
    """Выполнение всех запросов задания"""
    cursor = conn.cursor()

    print("1. Все возможные пары строк преподавателей и групп:")
    cursor.execute('''
        SELECT t.Name, t.Surname, g.Name 
        FROM Teachers t
        CROSS JOIN Groups g
    ''')
    for row in cursor.fetchall():
        print(f"   {row[0]} {row[1]} - {row[2]}")

    print("\n2. Факультеты, где фонд кафедр превышает фонд факультета:")
    cursor.execute('''
        SELECT f.Name 
        FROM Faculties f
        WHERE f.Financing < (
            SELECT SUM(d.Financing) 
            FROM Departments d 
            WHERE d.FacultyId = f.Id
        )
    ''')
    for row in cursor.fetchall():
        print(f"   {row[0]}")

    print("\n3. Кураторы групп и названия групп:")
    cursor.execute('''
        SELECT c.Surname, g.Name 
        FROM Curators c
        JOIN GroupsCurators gc ON c.Id = gc.CuratorId
        JOIN Groups g ON g.Id = gc.GroupId
    ''')
    for row in cursor.fetchall():
        print(f"   {row[0]} - {row[1]}")

    print("\n4. Преподаватели, читающие лекции у группы P107:")
    cursor.execute('''
        SELECT DISTINCT t.Name, t.Surname
        FROM Teachers t
        JOIN Lectures l ON t.Id = l.TeacherId
        JOIN GroupsLectures gl ON l.Id = gl.LectureId
        JOIN Groups g ON g.Id = gl.GroupId
        WHERE g.Name = 'P107'
    ''')
    for row in cursor.fetchall():
        print(f"   {row[0]} {row[1]}")

    print("\n5. Фамилии преподавателей и факультеты:")
    cursor.execute('''
        SELECT DISTINCT t.Surname, f.Name
        FROM Teachers t
        JOIN Lectures l ON t.Id = l.TeacherId
        JOIN GroupsLectures gl ON l.Id = gl.LectureId
        JOIN Groups g ON g.Id = gl.GroupId
        JOIN Departments d ON d.Id = g.DepartmentId
        JOIN Faculties f ON f.Id = d.FacultyId
    ''')
    for row in cursor.fetchall():
        print(f"   {row[0]} - {row[1]}")

    print("\n6. Кафедры и группы:")
    cursor.execute('''
        SELECT d.Name, g.Name
        FROM Departments d
        JOIN Groups g ON d.Id = g.DepartmentId
    ''')
    for row in cursor.fetchall():
        print(f"   {row[0]} - {row[1]}")

    print("\n7. Дисциплины преподавателя Samantha Adams:")
    cursor.execute('''
        SELECT DISTINCT s.Name
        FROM Subjects s
        JOIN Lectures l ON s.Id = l.SubjectId
        JOIN Teachers t ON t.Id = l.TeacherId
        WHERE t.Name = 'Samantha' AND t.Surname = 'Adams'
    ''')
    for row in cursor.fetchall():
        print(f"   {row[0]}")

    print("\n8. Кафедры, где читается Database Theory:")
    cursor.execute('''
        SELECT DISTINCT d.Name
        FROM Departments d
        JOIN Groups g ON d.Id = g.DepartmentId
        JOIN GroupsLectures gl ON g.Id = gl.GroupId
        JOIN Lectures l ON l.Id = gl.LectureId
        JOIN Subjects s ON s.Id = l.SubjectId
        WHERE s.Name = 'Database Theory'
    ''')
    for row in cursor.fetchall():
        print(f"   {row[0]}")

    print("\n9. Группы факультета Computer Science:")
    cursor.execute('''
        SELECT g.Name
        FROM Groups g
        JOIN Departments d ON d.Id = g.DepartmentId
        JOIN Faculties f ON f.Id = d.FacultyId
        WHERE f.Name = 'Computer Science'
    ''')
    for row in cursor.fetchall():
        print(f"   {row[0]}")

    print("\n10. Группы 5-го курса и их факультеты:")
    cursor.execute('''
        SELECT g.Name, f.Name
        FROM Groups g
        JOIN Departments d ON d.Id = g.DepartmentId
        JOIN Faculties f ON f.Id = d.FacultyId
        WHERE g.Year = 5
    ''')
    for row in cursor.fetchall():
        print(f"   {row[0]} - {row[1]}")

    print("\n11. Лекции в аудитории B103:")
    cursor.execute('''
        SELECT 
            t.Name || ' ' || t.Surname AS TeacherName,
            s.Name AS SubjectName,
            g.Name AS GroupName
        FROM Teachers t
        JOIN Lectures l ON t.Id = l.TeacherId
        JOIN Subjects s ON s.Id = l.SubjectId
        JOIN GroupsLectures gl ON l.Id = gl.LectureId
        JOIN Groups g ON g.Id = gl.GroupId
        WHERE l.LectureRoom = 'B103'
    ''')
    for row in cursor.fetchall():
        print(f"   {row[0]}: {row[1]} - {row[2]}")


def main():
    """Основная функция"""
    try:
        # Создание базы данных и подключение
        conn = create_database()

        print("=" * 60)
        print("РЕЗУЛЬТАТЫ ВЫПОЛНЕНИЯ ЗАПРОСОВ")
        print("=" * 60)

        # Выполнение запросов
        execute_queries(conn)

        # Закрытие соединения
        conn.close()
        print("\n" + "=" * 60)
        print("Все запросы выполнены успешно!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()