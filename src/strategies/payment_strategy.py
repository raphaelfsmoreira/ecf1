from abc import ABC, abstractmethod

from src.models.order import Order


class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, order: Order, amount_paid: float) -> bool:
        raise NotImplementedError
