import sqlite3

from src.database.database_interface import DatabaseInterface

class SQLiteDatabase(DatabaseInterface):

    def __init__(self):
        self.db = sqlite3.connect('loja.db')
        self.cursor = self.db.cursor()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def lastrowid(self) -> int:
        return int(self.cursor.lastrowid or 0)

    def commit(self):
        return self.db.commit()

    def close(self):
        self.db.close()

