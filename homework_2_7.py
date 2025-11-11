import sqlite3
import os
db_path = 'university.db'

def get_db_connection():
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS Groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                teacher TEXT
                );
            CREATE TABLE IF NOT EXISTS Students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                age INTEGER,
                group_id INTEGER,
                FOREIGN KEY (group_id) REFERENCES Groups (id)
                    ON DELETE SET NULL
                );
            CREATE TABLE IF NOT EXISTS Subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE
                );
            CREATE TABLE IF NOT EXISTS Grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                grade INTEGER NOT NULL CHECK (grade >= 1 AND grade <= 10),
                FOREIGN KEY (student_id) REFERENCES Students (id)
                    ON DELETE CASCADE,
                FOREIGN KEY (subject_id) REFERENCES Subjects (id)
                    ON DELETE CASCADE
                );
        ''')

class Group:
    tableName = 'Groups'
    def __init__(self, name, teacher, id=None):
        self.name = name
        self.teacher = teacher
        self.id = id
    def __repr__(self):
        return f"<Group (id={self.id}, name='{self.name}', teacher='{self.teacher}')>"
    def save(self):
        with get_db_connection() as conn:
            if self.id is None:
                cursor = conn.execute(
                    f"INSERT INTO {self.tableName} (name, teacher) VALUES (?, ?)",
                    (self.name, self.teacher)
                )
                self.id = cursor.lastrowid
            else:
                conn.execute(
                    f"UPDATE {self.tableName} SET name = ?, teacher = ? WHERE id = ?",
                    (self.name, self.teacher, self.id)
                )
    
    @classmethod
    def all(cls):
        with get_db_connection() as conn:
            cursor = conn.execute(f"SELECT * FROM {cls.tableName}")
            rows = cursor.fetchall()
            return [cls(id=r['id'], name=r['name'], teacher=r['teacher']) for r in rows]

class Student:
    tableName = "Students"

    def __init__(self, full_name, age, group_id, id=None):
        self.id = id
        self.full_name = full_name
        self.age = age
        self.group_id = group_id

    def __repr__(self):
        return f"<Student (id={self.id}, name='{self.full_name}', group_id={self.group_id})>"

    def save(self):
        with get_db_connection() as conn:
            if self.id is None:
                cursor = conn.execute(
                    f"INSERT INTO {self.tableName} (full_name, age, group_id) VALUES (?, ?, ?)",
                    (self.full_name, self.age, self.group_id)
                )
                self.id = cursor.lastrowid
            else:
                conn.execute(
                    f"UPDATE {self.tableName} SET full_name = ?, age = ?, group_id = ? WHERE id = ?",
                    (self.full_name, self.age, self.group_id, self.id)
                )

    @classmethod
    def all(cls):
        with get_db_connection() as conn:
            cursor = conn.execute(f"SELECT * FROM {cls.tableName}")
            rows = cursor.fetchall()
            return [cls(id=r['id'], full_name=r['full_name'], age=r['age'], group_id=r['group_id']) for r in rows]

class Subject:
    tableName = "Subjects"

    def __init__(self, title, id=None):
        self.id = id
        self.title = title

    def __repr__(self):
        return f"<Subject (id={self.id}, title='{self.title}')>"

    def save(self):
        with get_db_connection() as conn:
            if self.id is None:
                cursor = conn.execute(
                    f"INSERT INTO {self.tableName} (title) VALUES (?)",
                    (self.title,)
                )
                self.id = cursor.lastrowid
            else:
                conn.execute(
                    f"UPDATE {self.tableName} SET title = ? WHERE id = ?",
                    (self.title, self.id)
                )

    @classmethod
    def all(cls):
        with get_db_connection() as conn:
            cursor = conn.execute(f"SELECT * FROM {cls.tableName}")
            rows = cursor.fetchall()
            return [cls(id=r['id'], title=r['title']) for r in rows]

class Grade:
    tableName = "Grades"

    def __init__(self, student_id, subject_id, grade, id=None):
        self.id = id
        self.student_id = student_id
        self.subject_id = subject_id
        self.grade = grade

    def __repr__(self):
        return f"<Grade (id={self.id}, student={self.student_id}, subject={self.subject_id}, grade={self.grade})>"

    def save(self):
        with get_db_connection() as conn:
            if self.id is None:
                cursor = conn.execute(
                    f"INSERT INTO {self.tableName} (student_id, subject_id, grade) VALUES (?, ?, ?)",
                    (self.student_id, self.subject_id, self.grade)
                )
                self.id = cursor.lastrowid
            else:
                conn.execute(
                    f"UPDATE {self.tableName} SET student_id = ?, subject_id = ?, grade = ? WHERE id = ?",
                    (self.student_id, self.subject_id, self.grade, self.id)
                )

    @classmethod
    def all(cls):
        with get_db_connection() as conn:
            cursor = conn.execute(f"SELECT * FROM {cls.tableName}")
            rows = cursor.fetchall()
            return [cls(id=r['id'], student_id=r['student_id'], subject_id=r['subject_id'], grade=r['grade']) for r in rows]


def populate_data():
    print("\n--- Заполнение данными ---")
    try:
        g1 = Group(name="Backend-1", teacher="Анна Иванова")
        g1.save()
        g2 = Group(name="Frontend-2", teacher="Петр Сидоров")
        g2.save()

        s1 = Student(full_name="Иван Петров", age=20, group_id=g1.id)
        s1.save()
        s2 = Student(full_name="Мария Сидорова", age=22, group_id=g1.id)
        s2.save()
        s3 = Student(full_name="Алексей Смирнов", age=21, group_id=g2.id)
        s3.save()
        s4 = Student(full_name="Елена Козлова", age=23, group_id=g2.id)
        s4.save()

        sub1 = Subject(title="Python")
        sub1.save()
        sub2 = Subject(title="Базы данных")
        sub2.save()
        sub3 = Subject(title="JavaScript")
        sub3.save()

        Grade(student_id=s1.id, subject_id=sub1.id, grade=10).save()
        Grade(student_id=s1.id, subject_id=sub2.id, grade=8).save()
        Grade(student_id=s2.id, subject_id=sub1.id, grade=7).save()
        Grade(student_id=s2.id, subject_id=sub2.id, grade=7).save()
        Grade(student_id=s3.id, subject_id=sub2.id, grade=6).save()
        Grade(student_id=s3.id, subject_id=sub3.id, grade=9).save()
        Grade(student_id=s4.id, subject_id=sub2.id, grade=5).save()
        Grade(student_id=s4.id, subject_id=sub3.id, grade=10).save()

        print("Данные успешно добавлены.")
        print("\n--- Проверка .all() ---")
        print("Студенты:", Student.all())
        print("Группы:", Group.all())
        print("Оценки:", Grade.all())

    except Exception as e:
        print(f"Ошибка при заполнении данными: {e}")

def run_analytics():
    print("\n--- Выполнение SQL-запросов ---")
    with get_db_connection() as conn:
        cursor = conn.cursor()

        print("\n1. Средняя оценка каждого студента:")
        query1 = """
            SELECT s.full_name, ROUND(AVG(g.grade), 2) as avg_grade
            FROM Students s
            LEFT JOIN Grades g ON s.id = g.student_id
            GROUP BY s.id, s.full_name;
        """
        for row in cursor.execute(query1):
            print(f"   {row['full_name']}: {row['avg_grade']}")

        print("\n2. Средняя оценка по каждому предмету:")
        query2 = """
            SELECT s.title, ROUND(AVG(g.grade), 2) as avg_grade
            FROM Subjects s
            LEFT JOIN Grades g ON s.id = g.subject_id
            GROUP BY s.id, s.title;
        """
        for row in cursor.execute(query2):
            print(f"   {row['title']}: {row['avg_grade']}")

        print("\n3. Студенты со средней оценкой ВЫШЕ средней по их группе:")
        query3 = """
            WITH StudentAvg AS (
                SELECT student_id, AVG(grade) as student_avg_grade
                FROM Grades
                GROUP BY student_id
            ),
            GroupAvg AS (
                SELECT s.group_id, AVG(g.grade) as group_avg_grade
                FROM Grades g
                JOIN Students s ON g.student_id = s.id
                GROUP BY s.group_id
            )
            SELECT
                st.full_name,
                gr.name as group_name,
                ROUND(s_avg.student_avg_grade, 2) as student_avg,
                ROUND(g_avg.group_avg_grade, 2) as group_avg
            FROM Students st
            JOIN StudentAvg s_avg ON st.id = s_avg.student_id
            JOIN GroupAvg g_avg ON st.group_id = g_avg.group_id
            JOIN Groups gr ON st.group_id = gr.id
            WHERE s_avg.student_avg_grade > g_avg.group_avg_grade;
        """
        results = cursor.execute(query3).fetchall()
        if results:
            for row in results:
                print(f"   {row['full_name']} (Гр: {row['group_name']}) | Студ.Ср: {row['student_avg']} > Гр.Ср: {row['group_avg']}")
        else:
            print("   Таких студентов не найдено.")


        print("\n4. Создание VIEW 'ExcellentStudents' (ср. оценка >= 8)")
        try:
            conn.execute("DROP VIEW IF EXISTS ExcellentStudents;")
            view_query = """
                CREATE VIEW ExcellentStudents AS
                SELECT s.id, s.full_name, ROUND(AVG(g.grade), 2) as avg_grade
                FROM Students s
                JOIN Grades g ON s.id = g.student_id
                GROUP BY s.id, s.full_name
                HAVING AVG(g.grade) >= 8;
            """
            conn.execute(view_query)
            print("   VIEW 'ExcellentStudents' успешно создана.")

            print("\n    Содержимое 'ExcellentStudents':")
            for row in conn.execute("SELECT * FROM ExcellentStudents;"):
                print(f"     {row['full_name']} (ID: {row['id']}), Средний балл: {row['avg_grade']}")
        
        except Exception as e:
            print(f"   Ошибка при создании VIEW: {e}")


if __name__ == "__main__":
    init_db()
    populate_data()
    run_analytics()