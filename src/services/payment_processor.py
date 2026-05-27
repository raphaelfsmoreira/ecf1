from abc import ABC, abstractmethod

from src.models.order import Order


class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, order: Order, paid_amount: float) -> bool:
        """Process payment for an order and return True when accepted."""
        pass

    @abstractmethod
    def approves_immediately(self) -> bool:
        """Return True when accepted payment should set order status to approved."""
        pass
