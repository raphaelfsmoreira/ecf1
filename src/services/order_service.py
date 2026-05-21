from src.factories.order_factory import OrderFactory
from src.repositories.order_repository_interface import OrderRepositoryInterface
from src.models.order_item import OrderItem


class OrderService:
    def __init__(self, repository: OrderRepositoryInterface, factory: OrderFactory) -> None:
        self._repository = repository
        self._factory = factory

    def create_order(self, customer_name: str, items: list[OrderItem]) -> int:
        order = self._factory.create_order(customer_name, items)
        return self._repository.add_order(order)
