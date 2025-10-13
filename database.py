import sqlite3

class Database:
    def __init__(self, db_name='app.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                followers INTEGER,
                following INTEGER,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()  # <- Importante garantir que a tabela seja salva

    def add_user(self, username, followers, following):
        self.cursor.execute('''
            INSERT INTO users (username, followers, following)
            VALUES (?, ?, ?)
        ''', (username, followers, following))
        self.connection.commit()

    def close(self):
        self.connection.close()
