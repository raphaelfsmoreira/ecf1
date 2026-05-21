from enum import Enum

class OrderStatus(Enum):
    PENDING = "pendente"
    APPROVED = "aprovado"
    SENT = "enviado"
    DELIVERED = "entregue"
    CANCELLED = "cancelado"