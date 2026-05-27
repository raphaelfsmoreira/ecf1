import sqlite3
from sqlite3 import Cursor
from typing import Any, Sequence, cast

from src.database.database_interface import DatabaseInterface


class SQLiteDatabase(DatabaseInterface):

    def __init__(self, db_name: str = "loja.db") -> None:
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def execute(
        self,
        query: str,
        params: Sequence[Any] = (),
    ) -> Cursor:
        return self.cursor.execute(query, params)

    def fetchone(self) -> tuple[Any, ...] | None:
        return cast(tuple[Any, ...] | None, self.cursor.fetchone())

    def fetchall(self) -> list[tuple[Any, ...]]:
        return cast(list[tuple[Any, ...]], self.cursor.fetchall())

    def commit(self) -> None:
        self.connection.commit()

    def lastrowid(self) -> int:
        last_id = self.cursor.lastrowid

        if last_id is None:
            raise RuntimeError(
                "No row was inserted before requesting lastrowid"
            )

        return last_id

    def close(self) -> None:
        self.connection.close()
