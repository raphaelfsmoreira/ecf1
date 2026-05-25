import sqlite3
from typing import Any, List, Sequence

from src.database.database_interface import DatabaseInterface


class SQLiteDatabase(DatabaseInterface):

    def __init__(self) -> None:
        self.db: sqlite3.Connection = sqlite3.connect('loja.db')
        self.cursor: sqlite3.Cursor = self.db.cursor()

    def execute(self, query: str, params: Sequence[Any] = ()) -> None:
        self.cursor.execute(query, params)

    def fetchone(self) -> Any:
        return self.cursor.fetchone()

    def fetchall(self) -> list[Any]:
        return self.cursor.fetchall()

    def lastrowid(self) -> int:
        return int(self.cursor.lastrowid or 0)

    def commit(self) -> None:
        self.db.commit()

    def close(self) -> None:
        self.db.close()

