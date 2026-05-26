from src.models.order_item import OrderItem
from src.strategies.discount_strategy import DiscountStrategy
from src.strategies.item_discount_strategy import ItemDiscountStrategy
from src.strategies.volume_discount_strategy import VolumeDiscountStrategy


class DiscountService:
    def __init__(self, strategies: list[DiscountStrategy] | None = None) -> None:
        self._strategies = strategies or [
            ItemDiscountStrategy(),
            VolumeDiscountStrategy(),
        ]

    def calculate_item_total(self, item: OrderItem) -> float:
        total = item.unit_price * item.quantity

        for strategy in self._strategies:
            total = strategy.apply(item, total)

        return total

    def calculate_items_total(self, items: list[OrderItem]) -> float:
        return sum(self.calculate_item_total(item) for item in items)
