from src.models.order import Order
from src.observers.notification_observer import NotificationObserver


class EmailNotificationObserver(NotificationObserver):
    def notify(self, order: Order, message: str) -> None:
        print(f"Email enviado para {order.customer_name}: {message}")


class SmsNotificationObserver(NotificationObserver):
    def notify(self, order: Order, message: str) -> None:
        print(f"SMS enviado para {order.customer_name}: {message}")


class AccountManagerNotificationObserver(NotificationObserver):
    def notify(self, order: Order, message: str) -> None:
        print(f"Notificação enviada ao gerente de conta de {order.customer_name}: {message}")


class WhatsAppNotificationObserver(NotificationObserver):
    def notify(self, order: Order, message: str) -> None:
        print(f"WhatsApp enviado para {order.customer_name}: {message}")
