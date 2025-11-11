import sqlite3

class DataBaseManager:
    def __init__(self, db_name='students.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                age INTEGER,
                student_id TEXT UNIQUE
                );
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            teacher_id INTEGER
            );
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER,
            grade REAL
            );
        ''')
        self.conn.commit()

    def add_student(self, first_name, last_name, age, student_id):
        self.cursor.execute('''
            INSERT INTO students (first_name, last_name, age, student_id)
            VALUES (?,?,?,?)
        ''', (first_name, last_name, age, student_id))
        self.conn.commit()

    def list_student(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def add_grade(self, student_id, course_id, grade):
        self.cursor.execute('''
            INSERT INTO grades (student_id, course_id, grade)
            VALUES (?, ?, ?)
        ''', (student_id, course_id, grade))
        self.conn.commit()

    def get_average_by_Course(self):
        self.cursor.execute('''
            SELECT c.name, AVG(g.grade)
            FROM grades g
            JOIN courses c ON g.course_id = c.id
            GROUP BY c.name;
        ''')
        return self.cursor.fetchall()