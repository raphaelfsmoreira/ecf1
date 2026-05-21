from abc import ABC, abstractmethod
from typing import Any, Sequence

# Interface de Database
# Cria o contrato de implementação de um banco de dados relacional
# Isso permite que o projeto possa expandir ou trocar de banco se houver necessidade.
# Bastaria chamar um SQLiteDatabase() ou um OracleDatabase() ou etc.
# Torna o projeto plug and play nesse quesito...
class DatabaseInterface(ABC):

    @abstractmethod
    def execute(self, query: str, params: Sequence[Any] = ()) -> None:
        pass

    @abstractmethod
    def fetchone(self) -> Any:
        pass

    @abstractmethod
    def fetchall(self) -> list[Any]:
        pass

    @abstractmethod
    def lastrowid(self) -> int:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
