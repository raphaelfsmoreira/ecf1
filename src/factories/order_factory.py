from abc import ABC, abstractmethod
from datetime import datetime

from src.models.order import Order
from src.models.order_item import OrderItem
from src.models.enums import CustomerType, OrderStatus
from src.services.discount_service import DiscountService

'''
A ordem de aplicação de descontos segue:

1. calcula total dos itens
2. aplica descontos dos itens, incluindo volume (utilizando discountService que é ditado pelo strategy)
3. depois aplica desconto do tipo de cliente 


'''


class OrderFactory(ABC):
    @abstractmethod
    def create_order(self, customer_name: str, items: list[OrderItem]) -> Order:
        pass

    def __init__(self, discount_service: DiscountService | None = None) -> None:
        self._discount_service = discount_service or DiscountService()

    def _calculate_items_total(self, items: list[OrderItem]) -> float:
        return self._discount_service.calculate_items_total(items)


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
