import sqlite3
from contextlib import contextmanager

DB_NAME = 'todolist.db'

@contextmanager
def get_connection(db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    try:
        yield conn
    finally:
        conn.close()

class Database:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self._temp_conn = sqlite3.connect(self.db_name)
        self.create_table()

    def create_table(self):
        with get_connection(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute('''
            CREATE TABLE IF NOT EXISTS todolist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                is_done INTEGER DEFAULT 0
            )
            ''')
            conn.commit()

    def add_task(self, title):
        with get_connection(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO todolist (title, is_done) VALUES (?, 0)", (title,))
            conn.commit()

    def get_all_tasks(self):
        with get_connection(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute('SELECT id, title, is_done FROM todolist')
            rows = cur.fetchall()
            return rows

    def update_status(self, task_id, is_done):
        with get_connection(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute("UPDATE todolist SET is_done = ? WHERE id = ?", (is_done, task_id))
            conn.commit()

    def delete_task(self, task_id):
        with get_connection(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute('DELETE FROM todolist WHERE id = ?', (task_id,))
            conn.commit()
            
    def close(self):
        self._temp_conn.close()