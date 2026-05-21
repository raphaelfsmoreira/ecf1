from abc import ABC, abstractmethod
from datetime import datetime

from src.models.order import Order
from src.models.order_item import OrderItem
from src.models.enums import CustomerType, DiscountType, OrderStatus


class OrderFactory(ABC):
    @abstractmethod
    def create_order(self, customer_name: str, items: list[OrderItem]) -> Order:
        pass

    def _calculate_items_total(self, items: list[OrderItem]) -> float:
        total = 0.0
        for item in items:
            if item.discount_type in (DiscountType.NORMAL, DiscountType.FREE_SHIPPING):
                total += item.unit_price * item.quantity
            elif item.discount_type == DiscountType.DISCOUNT_10:
                total += item.unit_price * item.quantity * 0.9
            elif item.discount_type == DiscountType.DISCOUNT_20:
                total += item.unit_price * item.quantity * 0.8
        return total


class NormalOrderFactory(OrderFactory):
    def create_order(self, customer_name: str, items: list[OrderItem]) -> Order:
        total = self._calculate_items_total(items)
        return Order(
            customer_name=customer_name,
            items=items,
            total_amount=total,
            status=OrderStatus.PENDING,
            created_at=datetime.now(),
            customer_type=CustomerType.NORMAL,
        )


class VipOrderFactory(OrderFactory):
    _DISCOUNT = 0.95

    def create_order(self, customer_name: str, items: list[OrderItem]) -> Order:
        total = self._calculate_items_total(items) * self._DISCOUNT
        return Order(
            customer_name=customer_name,
            items=items,
            total_amount=total,
            status=OrderStatus.PENDING,
            created_at=datetime.now(),
            customer_type=CustomerType.VIP,
        )


class CorporateOrderFactory(OrderFactory):
    _DISCOUNT = 0.9

    def create_order(self, customer_name: str, items: list[OrderItem]) -> Order:
        total = self._calculate_items_total(items) * self._DISCOUNT
        return Order(
            customer_name=customer_name,
            items=items,
            total_amount=total,
            status=OrderStatus.PENDING,
            created_at=datetime.now(),
            customer_type=CustomerType.CORPORATIVE,
        )


_FACTORIES: dict[CustomerType, OrderFactory] = {
    CustomerType.NORMAL: NormalOrderFactory(),
    CustomerType.VIP: VipOrderFactory(),
    CustomerType.CORPORATIVE: CorporateOrderFactory(),
}


def get_order_factory(customer_type: CustomerType) -> OrderFactory:
    factory = _FACTORIES.get(customer_type)
    if factory is None:
        raise ValueError(f'No factory registered for customer type: {customer_type}')
    return factory
