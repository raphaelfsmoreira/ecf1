from dataclasses import dataclass
from datetime import datetime

from src.factories.order_factory import OrderFactory
from src.models.enums import CustomerType, DiscountType, OrderStatus
from src.models.order import Order
from src.models.order_item import OrderItem
from src.observers.notification_observer import NotificationObserver
from src.observers.notification_publisher import NotificationPublisher
from src.repositories.order_repository_interface import OrderRepositoryInterface
from src.services.order_service import OrderService


class InMemoryOrderRepository(OrderRepositoryInterface):
    def __init__(self) -> None:
        self.saved_orders: list[Order] = []

    def add_order(self, order: Order) -> int:
        self.saved_orders.append(order)
        return len(self.saved_orders)

    def get_order_by_id(self, order_id: int) -> Order | None:
        if 1 <= order_id <= len(self.saved_orders):
            return self.saved_orders[order_id - 1]
        return None

    def update_status(self, order_id: int, status: OrderStatus) -> None:
        order = self.get_order_by_id(order_id)
        if order is not None:
            order.status = status

    def calculate_total_amount_by_customer_name(self, customer_name: str) -> float:
        return sum(order.total_amount for order in self.saved_orders if order.customer_name == customer_name)

    def cancel_order(self, order_id: int) -> None:
        self.update_status(order_id, OrderStatus.CANCELLED)


class RecordingPublisher(NotificationPublisher):
    def __init__(self) -> None:
        self.subscribers: list[NotificationObserver] = []
        self.published_orders: list[Order] = []

    def subscribe(self, observer: NotificationObserver) -> None:
        self.subscribers.append(observer)

    def unsubscribe(self, observer: NotificationObserver) -> None:
        self.subscribers = [item for item in self.subscribers if item is not observer]

    def publish(self, order: Order) -> None:
        self.published_orders.append(order)


class FixedOrderFactory(OrderFactory):
    def create_order(
        self,
        customer_name: str,
        items: list[OrderItem],
        customer_type: CustomerType,
    ) -> Order:
        return Order(
            customer_name=customer_name,
            items=items,
            total_amount=245.0,
            status=OrderStatus.PENDING,
            created_at=datetime(2026, 5, 22, 12, 0, 0),
            customer_type=customer_type,
        )


def test_order_service_places_and_publishes_order() -> None:
    repository = InMemoryOrderRepository()
    publisher = RecordingPublisher()
    factory = FixedOrderFactory()

    service = OrderService(repository, factory, publisher)

    order_id = service.place_order(
        customer_name="Joao Silva",
        items=[OrderItem("produto1", 100.0, 1, DiscountType.NORMAL)],
        customer_type=CustomerType.NORMAL,
    )

    assert order_id == 1
    assert len(repository.saved_orders) == 1
    assert repository.saved_orders[0].customer_name == "Joao Silva"
    assert len(publisher.published_orders) == 1
    assert publisher.published_orders[0].total_amount == 245.0