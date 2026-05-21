import sqlite3


# Interface de Database
# Cria o contrato de implementação de um banco de dados relacional
# Isso permite que o projeto possa expandir ou trocar de banco se houver necessidade.
# Bastaria chamar um SQLiteDatabase() ou um OracleDatabase() ou etc.
# Torna o projeto plug and play nesse quesito...
class Database():

    def execute(self, query, params=None):
        pass

    def fetchone(self):
        pass

    def fetchall(self):
        pass

    def lastrowid(self):
        pass

    def commit(self):
        pass

    def close(self):
        pass


class SQLiteDatabase(Database):

    def __init__(self):
        self.db = sqlite3.connect('loja.db')
        self.cursor = self.db.cursor()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def lastrowid(self):
        return self.cursor.lastrowid

    def commit(self):
        return self.db.commit()

    def close(self):
        self.db.close()

