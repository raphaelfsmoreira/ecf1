from abc import ABC, abstractmethod

from src.models.order_item import OrderItem


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, item: OrderItem, current_total: float) -> float:
        pass
