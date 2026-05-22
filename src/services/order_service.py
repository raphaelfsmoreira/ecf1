from abc import ABC, abstractmethod

from src.factories.order_factory import OrderFactory
from src.models.enums import CustomerType
from src.models.order_item import OrderItem
from src.observers.notification_publisher import NotificationPublisher
from src.repositories.order_repository_interface import OrderRepositoryInterface


class OrderServiceInterface(ABC):
    @abstractmethod
    def place_order(
        self,
        customer_name: str,
        items: list[OrderItem],
        customer_type: CustomerType,
    ) -> int:
        raise NotImplementedError


class OrderService(OrderServiceInterface):
    def __init__(
        self,
        repository: OrderRepositoryInterface,
        factory: OrderFactory,
        publisher: NotificationPublisher,
    ) -> None:
        self._repository = repository
        self._factory = factory
        self._publisher = publisher

    def place_order(
        self,
        customer_name: str,
        items: list[OrderItem],
        customer_type: CustomerType,
    ) -> int:
        order = self._factory.create_order(customer_name, items, customer_type)
        order_id = self._repository.add_order(order)
        self._publisher.publish(order)
        return order_id