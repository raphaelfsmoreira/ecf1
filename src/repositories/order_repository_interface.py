from abc import ABC, abstractmethod

from src.models.order import Order
from src.models.enums import OrderStatus


# Definindo o contrato do Repositorio de Pedidos...
class OrderRepositoryInterface(ABC):

    @abstractmethod
    def add_order(self, order: Order) -> int:
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: int) -> Order | None:
        pass

    @abstractmethod
    def update_status(self, order_id: int, status: OrderStatus) -> None:
        pass

    @abstractmethod
    def calculate_total_amount_by_customer_name(self, customer_name: str) -> float:
        pass

    @abstractmethod
    def cancel_order(self, order_id: int) -> None:
        pass