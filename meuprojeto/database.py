import sqlite3
from threading import Lock

class Database:
    _lock = Lock()

    def __init__(self, db_name='app.db'):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name, check_same_thread=False)

    def create_table(self):
        with Database._lock:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        followers INTEGER,
                        following INTEGER,
                        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()

    # adiciona ou atualiza automaticamente
    def add_or_update_user(self, username, followers, following):
        with Database._lock:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (username, followers, following)
                    VALUES (?, ?, ?)
                    ON CONFLICT(username) DO UPDATE SET
                        followers = excluded.followers,
                        following = excluded.following,
                        date_added = CURRENT_TIMESTAMP
                """, (username, followers, following))
                conn.commit()

    def get_user(self, username):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT username, followers, following, date_added
                FROM users WHERE username = ?
                ORDER BY date_added DESC LIMIT 1
            """, (username,))
            result = cursor.fetchone()
            if result:
                return {"username": result[0], "followers": result[1], "following": result[2], "date": result[3]}
            return None

    def compare_user(self, username, followers, following):
        old = self.get_user(username)
        if not old:
            return {"diff_followers": 0, "diff_following": 0}
        return {
            "diff_followers": followers - old["followers"],
            "diff_following": following - old["following"],
        }

    def list_users(self, limit=10):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT username, followers, following, date_added
                FROM users
                ORDER BY date_added DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [{"username": r[0], "followers": r[1], "following": r[2], "date": r[3]} for r in rows]
