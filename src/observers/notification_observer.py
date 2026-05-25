from abc import ABC, abstractmethod

from src.models.order import Order


class NotificationObserver(ABC):
    @abstractmethod
    def update(self, order: Order) -> None:
        raise NotImplementedError
