from abc import ABC, abstractmethod

from src.models.order import Order


class DiscountStrategy(ABC):
    @abstractmethod
    def calculate_total(self, order: Order) -> float:
        raise NotImplementedError
