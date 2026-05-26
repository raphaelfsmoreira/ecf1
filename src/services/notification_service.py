from collections.abc import Sequence

from src.models.enums import CustomerType
from src.models.order import Order
from src.observers.notification_observer import NotificationObserver
from src.observers.notification_channels import (
    AccountManagerNotificationObserver,
    EmailNotificationObserver,
    SmsNotificationObserver,
    WhatsAppNotificationObserver,
)


class NotificationService:
    def __init__(
        self,
        default_observers: Sequence[NotificationObserver],
        customer_observers: dict[CustomerType, Sequence[NotificationObserver]] | None = None,
    ) -> None:
        self._default_observers = list(default_observers)
        self._customer_observers = customer_observers or {}

    def notify(self, order: Order, message: str) -> None:
        observers = [
            *self._default_observers,
            *self._customer_observers.get(order.customer_type, []),
        ]
        for observer in observers:
            observer.notify(order, message)


def create_default_notification_service() -> NotificationService:
    return NotificationService(
        default_observers=[
            EmailNotificationObserver(),
            WhatsAppNotificationObserver(),
        ],
        customer_observers={
            CustomerType.VIP: [SmsNotificationObserver()],
            CustomerType.CORPORATIVE: [AccountManagerNotificationObserver()],
        },
    )
