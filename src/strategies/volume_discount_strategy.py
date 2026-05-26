from src.models.order_item import OrderItem
from src.strategies.discount_strategy import DiscountStrategy


class VolumeDiscountStrategy(DiscountStrategy):
    MINIMUM_QUANTITY = 3
    DISCOUNT_FACTOR = 0.85

    def apply(self, item: OrderItem, current_total: float) -> float:
        if item.quantity >= self.MINIMUM_QUANTITY:
            return current_total * self.DISCOUNT_FACTOR

        return current_total
