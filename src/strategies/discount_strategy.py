from abc import ABC, abstractmethod

from src.models.enums import DiscountType
from src.models.order_item import OrderItem


class DiscountStrategy(ABC):
    @abstractmethod
    def calculate_total(self, item: OrderItem) -> float:
        raise NotImplementedError


class NoDiscountStrategy(DiscountStrategy):
    def calculate_total(self, item: OrderItem) -> float:
        return item.unit_price * item.quantity


class TenPercentDiscountStrategy(DiscountStrategy):
    def calculate_total(self, item: OrderItem) -> float:
        return item.unit_price * item.quantity * 0.9


class TwentyPercentDiscountStrategy(DiscountStrategy):
    def calculate_total(self, item: OrderItem) -> float:
        return item.unit_price * item.quantity * 0.8


class FreeShippingDiscountStrategy(DiscountStrategy):
    def calculate_total(self, item: OrderItem) -> float:
        return item.unit_price * item.quantity


class ProgressiveVolumeDiscountStrategy(DiscountStrategy):
    def calculate_total(self, item: OrderItem) -> float:
        subtotal = item.unit_price * item.quantity
        if item.quantity >= 3:
            return subtotal * 0.85
        return subtotal


def strategy_for_discount_type(discount_type: DiscountType) -> DiscountStrategy:
    if discount_type is DiscountType.DISCOUNT_10:
        return TenPercentDiscountStrategy()
    if discount_type is DiscountType.DISCOUNT_20:
        return TwentyPercentDiscountStrategy()
    if discount_type is DiscountType.FREE_SHIPPING:
        return FreeShippingDiscountStrategy()
    return NoDiscountStrategy()
