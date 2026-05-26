from src.models.enums import DiscountType
from src.models.order_item import OrderItem
from src.strategies.discount_strategy import DiscountStrategy


class ItemDiscountStrategy(DiscountStrategy):
    def apply(self, item: OrderItem, current_total: float) -> float:
        if item.discount_type == DiscountType.DISCOUNT_10:
            return current_total * 0.9

        if item.discount_type == DiscountType.DISCOUNT_20:
            return current_total * 0.8

        return current_total
