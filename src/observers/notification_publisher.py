from abc import ABC, abstractmethod

from src.models.order import Order

from src.observers.notification_observer import NotificationObserver


class NotificationPublisher(ABC):
    @abstractmethod
    def subscribe(self, observer: NotificationObserver) -> None:
        raise NotImplementedError

    @abstractmethod
    def unsubscribe(self, observer: NotificationObserver) -> None:
        raise NotImplementedError

    @abstractmethod
    def publish(self, order: Order) -> None:
        raise NotImplementedError
