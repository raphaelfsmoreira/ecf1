from dataclasses import dataclass

from src.models.enums import DiscountType


# Dataclass dos Itens do Pedido.
# Anteriormente os itens eram representados como um dict solto, isso dentro do Clean Code é considerado
# um Code Smell. Os Itens que compõem um pedido têm uma estrutura própria.
@dataclass
class OrderItem:
    product_name: str
    unit_price: float
    quantity: int
    discount_type: DiscountType