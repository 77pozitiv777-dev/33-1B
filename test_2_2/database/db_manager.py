import sqlite3
class DataBaseManager:
    def __init__(self, db_name='library.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
    def create_tables(self):
        self.cursor.exucute('''
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE,
                biography TEXT
                );
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS readers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE,
                number_of_reader_ticket INTEGER
                );
        ''')
        self.cursor.execute('''

            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                genre TEXT,
                author TEXT
                );
        ''')

def add_author(self, name, email, biography):
    self.name = name
    self.email = email
    self.biography = biography
    self.cursor.exucute('''
            INSERT INTO authors (name, email, biography)
            VALUES (?, ?, ?)
        ''', (name, email, biography))
    self.conn.commit()

def get_all_authors(self):
    self.cursor.execute('SELECT * FROM authors')
    return self.cursor.fetchall()

def delete_data_of_author(self, author_id):
    self.cursor.execute('DELETE FROM authors WHERE id = ?', (author_id,))
    self.conn.commit()

def update_data_of_author(self, author_id, name=None, email=None, biography=None):
    if name:
        self.cursor.execute('UPDATE authors SET name = ? WHERE id = ?', (name, author_id))
    if email:
        self.cursor.execute('UPDATE authors SET email = ? WHERE id = ?', (email, author_id))
    if biography:
        self.cursor.execute('UPDATE authors SET biography = ? WHERE id = ?', (biography, author_id))
        self.conn.commit()

def register_reader(self, name, email, number_of_reader_ticket):
    self.name = name
    self.email = email
    self.number_of_reader_ticket = number_of_reader_ticket
    self.cursor.execute('''
        INSERT INTO READERS (name, email, number_of_reader_ticket)
        VALUES (?, ?, ?)
        ''', (name, email, number_of_reader_ticket))
    self.conn.commit()

def get_all_readers(self):
    self.cursor.execute('SELECT * FROM readers')
    return self.cursor.fetchall()

def delete_data_of_reader(self, reader_id):
    self.cursor.execute('DELETE FROM readers WHERE id = ?', (reader_id,))
    self.conn.commit()

def update_data_of_reader(self, reader_id=None, name=None, email=None, number_of_reader_ticket=None):
    if name:
        self.cursor.execute('UPDATE readers SET name = ? WHERE id = ?', (name, reader_id))
    if email:
        self.cursor.execute('UPDATE readers SET email = ? WHERE id = ?', (email, reader_id))
    if number_of_reader_ticket:
        self.cursor.execute('UPDATE readers SET number_of_reader_ticket = ? WHERE id = ?', (number_of_reader_ticket, reader_id))
        self.conn.commit()

def add_book(self, title, genre, author):
    self.title = title
    self.genre = genre
    self.author = author
    self.cursor.execute('''
            INSERT INTO books (title, genre, author)
            values (?, ?, ?)
        ''')
    self.conn.commit()

def get_all_books(self):
    self.cursor.execute('SELECT * FROM books')
    return self.cursor.fetchall()

def filter_books(self, genre=None, author=None, is_borrowed=None):
    query = 'SELECT * FROM books WHERE 1=1'
    params = []
    if genre:
        query += ' AND genre = ?'
        params.append(genre)
    if author:
        query += ' AND author = ?'
        params.append(author)
    if is_borrowed is not None:
        query += ' AND is_borrowed = ?'
        params.append(is_borrowed)
    self.cursor.execute(query, tuple(params))
    return self.cursor.fetchall()

def delete_data_of_book(self, book_id):
    self.cursor.execute('DELETE FROM books WHERE id = ?', (book_id))
    self.conn.commit()

def update_data_of_book(self, book_id, title=None, genre=None, author=None):
    if title:
        self.cursor.execute('UPDATE books SET title = ? WHERE id = ?', (title, book_id))
    if genre:
        self.cursor.execute('UPDATE books SET genre = ? WHERE id = ?', (genre, book_id))
    if author:
        self. cursor.execute('UPDATE books SET author = ? WHERE id = ?', (author, book_id))
    self.conn.commit()

def borrow_book(self, book_id):
    self.cursor.execute('UPDATE books SET is_borrowed = 1 WHERE id = ?', (book_id,))
    self.conn.commit()

def return_book(self, book_id):
    self.cursor.execute('UPDATE books SET is_borrowed = 0 WHERE id = ?', (book_id,))
    self.conn.commit()

def is_book_available(self, book_id):
    self.cursor.execute('SELECT is_borrowed FROM books WHERE id = ?', (book_id,))
    status = self.cursor.fetchone()
    return status[0] == 0

def count_books_by_genre(self):
    self.cursor.execute('''
        SELECT genre, COUNT(*) as count
        FROM books
        GROUP BY genre
    ''')
    return self.cursor.fetchall()

def authors_with_more_than_three_books(self):
    self.cursor.execute('''
        SELECT name
        FROM authors
        WHERE id IN (
            SELECT author
            FROM books
            GROUP BY author
            HAVING COUNT(*) > 3
        )
    ''')
    return self.cursor.fetchall()

def create_borrowed_books_view(self):
    self.cursor.execute('''
        CREATE VIEW IF NOT EXISTS borrowed_books AS
        SELECT b.title, a.name as author_name, r.name as reader_name
        FROM books b
        JOIN authors a ON b.authors = a.id
        JOIN readers r ON b.borrowed_by = r.id
        WHERE b.is_borrowed = 1)
        ''')
    self.conn.commit()