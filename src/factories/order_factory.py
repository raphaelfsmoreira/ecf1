from abc import ABC, abstractmethod
from collections.abc import Callable
from datetime import datetime

from src.models.enums import CustomerType, OrderStatus
from src.models.order import Order
from src.models.order_item import OrderItem
from src.services.order_pricing_service import calculate_order_total


class OrderFactory(ABC):
    @abstractmethod
    def create_order(
        self,
        customer_name: str,
        items: list[OrderItem],
        customer_type: CustomerType,
    ) -> Order:
        raise NotImplementedError


class DefaultOrderFactory(OrderFactory):
    def __init__(self, now_provider: Callable[[], datetime] | None = None) -> None:
        self._now_provider = now_provider or datetime.now

    def create_order(
        self,
        customer_name: str,
        items: list[OrderItem],
        customer_type: CustomerType,
    ) -> Order:
        order = Order(
            customer_name=customer_name,
            items=items,
            total_amount=0.0,
            status=OrderStatus.PENDING,
            created_at=self._now_provider(),
            customer_type=customer_type,
        )

        return Order(
            customer_name=order.customer_name,
            items=order.items,
            total_amount=calculate_order_total(order),
            status=order.status,
            created_at=order.created_at,
            customer_type=order.customer_type,
        )