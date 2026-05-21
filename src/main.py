from src.database.database import SQLiteDatabase
from src.database.schema import create_tables


def main():
    # Definindo o Database
    db = SQLiteDatabase()

    # Inicializando as tabelas a partir do schema
    create_tables(db)


if __name__ == '__main__':
    main()