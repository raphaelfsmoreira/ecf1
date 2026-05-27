from src.models.enums import CustomerType
from src.observers.notification_channels import (
    AccountManagerNotificationObserver,
    EmailNotificationObserver,
    SmsNotificationObserver,
    WhatsAppNotificationObserver,
)
from src.observers.notification_observer import NotificationObserver
from src.services.notification_service import NotificationService


class NotificationFactory:
    """Factory responsável por montar os canais de notificação por tipo de cliente."""

    @staticmethod
    def create_for_customer(customer_type: CustomerType) -> NotificationService:
        observers: list[NotificationObserver] = [
            EmailNotificationObserver(),
            WhatsAppNotificationObserver(),
        ]

        if customer_type == CustomerType.VIP:
            observers.append(SmsNotificationObserver())
        elif customer_type == CustomerType.CORPORATIVE:
            observers.append(AccountManagerNotificationObserver())

        return NotificationService(observers)
