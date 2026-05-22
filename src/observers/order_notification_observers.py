from src.models.enums import CustomerType
from src.models.order import Order
from src.observers.notification_observer import NotificationObserver
from src.observers.notification_publisher import NotificationPublisher


class EmailNotificationObserver(NotificationObserver):
    def update(self, order: Order) -> None:
        print(f"Email enviado para {order.customer_name}: Pedido recebido!")


class SmsNotificationObserver(NotificationObserver):
    def update(self, order: Order) -> None:
        if order.customer_type == CustomerType.VIP:
            print(f"SMS enviado para {order.customer_name}: Pedido VIP recebido!")


class AccountManagerNotificationObserver(NotificationObserver):
    def update(self, order: Order) -> None:
        if order.customer_type == CustomerType.CORPORATIVE:
            print(f"Notificação enviada ao gerente de conta de {order.customer_name}")


class WhatsAppNotificationObserver(NotificationObserver):
    def update(self, order: Order) -> None:
        print(f"WhatsApp enviado para {order.customer_name}: Pedido recebido!")


class OrderNotificationPublisher(NotificationPublisher):
    def __init__(self) -> None:
        self._observers: list[NotificationObserver] = []

    def subscribe(self, observer: NotificationObserver) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: NotificationObserver) -> None:
        self._observers = [item for item in self._observers if item is not observer]

    def publish(self, order: Order) -> None:
        for observer in self._observers:
            observer.update(order)