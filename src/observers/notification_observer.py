from abc import ABC, abstractmethod

from src.models.order import Order


class NotificationObserver(ABC):
    @abstractmethod
    def notify(self, order: Order, message: str) -> None:
        pass
