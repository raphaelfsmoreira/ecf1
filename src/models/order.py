from dataclasses import dataclass
from datetime import datetime

# Import dos Enums
from src.models.enums import CustomerType, OrderStatus

# Import do Modelo de Item
from src.models.order_item import OrderItem

# Dataclass do Pedido

@dataclass
class Order:
    customer_name: str

    # Para o objeto Order, os itens serão uma lista de objetos OrderItem.
    # Porém, ao gravar no banco, primeiro deve ser seriliazado para JSON
    # E lido do banco, transformado de JSON para o objeto OrderItem.
    # Ou seja, não enviar ou receber o objeto ao banco e sim seu conteúdo...
    items: list[OrderItem]

    total_amount: float
    status: OrderStatus
    created_at: datetime

    customer_type: CustomerType

    # Id pode ser None, pois o objeto primeiro é criado e depois o SQLite
    # atribui um id para ele.
    # Deixar como int só no caso futuro se quiser atribuir um id previamente ao objeto.
    id: int | None = None