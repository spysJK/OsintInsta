import sqlite3
from threading import Lock

class Database:
    _lock = Lock()  # garante segurança de acesso simultâneo

    def __init__(self, db_name='app.db'):
        self.db_name = db_name

    def connect(self):
        """Abre uma nova conexão segura por operação"""
        # check_same_thread=False permite acesso entre threads
        return sqlite3.connect(self.db_name, check_same_thread=False)

    def create_table(self):
        with Database._lock:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        followers INTEGER,
                        following INTEGER,
                        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()

    def add_user(self, username, followers, following):
        with Database._lock:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, followers, following)
                    VALUES (?, ?, ?)
                ''', (username, followers, following))
                conn.commit()

    def comparacao_followers(self, username):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT followers FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            return result[0] if result else ""

    def comparacao_folliwing(self, username):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT following FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            return result[0] if result else ""
    def get_latest_followers(self, username):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT followers
                FROM users
                WHERE username = ?
                ORDER BY date_added DESC
                LIMIT 1
            """, (username,))
            result = cursor.fetchone()
            return result[0] if result else 0

    def get_latest_following(self, username):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT following
                FROM users
                WHERE username = ?
                ORDER BY date_added DESC
                LIMIT 1
            """, (username,))
            result = cursor.fetchone()
            return result[0] if result else 0
