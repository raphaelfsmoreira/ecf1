from src.database.database import SQLiteDatabase
from src.database.schema import create_tables
from src.factories.order_factory import DefaultOrderFactory
from src.observers.order_notification_observers import (
    AccountManagerNotificationObserver,
    EmailNotificationObserver,
    OrderNotificationPublisher,
    SmsNotificationObserver,
    WhatsAppNotificationObserver,
)
from src.repositories.order_repository import OrderRepository
from src.services.order_service import OrderService
from src.services.payment_service import PaymentService


def build_application() -> tuple[OrderService, PaymentService]:
    db = SQLiteDatabase()
    create_tables(db)

    repository = OrderRepository(db)
    factory = DefaultOrderFactory()

    publisher = OrderNotificationPublisher()
    publisher.subscribe(EmailNotificationObserver())
    publisher.subscribe(SmsNotificationObserver())
    publisher.subscribe(AccountManagerNotificationObserver())
    publisher.subscribe(WhatsAppNotificationObserver())

    order_service = OrderService(repository, factory, publisher)
    payment_service = PaymentService(repository)

    return order_service, payment_service


def main() -> None:
    build_application()


if __name__ == '__main__':
    main()