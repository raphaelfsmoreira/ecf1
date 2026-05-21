# Em projetos reais o banco já vai estar inicializado... Então essa parte
# de infraestrutura não estaria no código.
# Lembrar de inicializar a tabela no início da aplicação na main.py.

# Deve ser aplicado Clean Code aqui também. Os atributos da tabela foram renomeados para maior clareza.
"""
cli = customer_name
tot = total_amount
st = status
dt = created_at
tp = payment_type
"""

def create_tables(db):
    db.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            items TEXT NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            customer_type TEXT NOT NULL
        )
    """)
    db.commit()