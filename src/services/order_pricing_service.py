from src.models.enums import CustomerType as CustomerTypeEnum
from src.models.order import Order
from src.models.order_item import OrderItem
from src.strategies.discount_strategy import DiscountStrategy, strategy_for_discount_type


def calculate_order_total(order: Order) -> float:
    total = 0.0
    for item in order.items:
        strategy: DiscountStrategy = strategy_for_discount_type(item.discount_type)
        total += strategy.calculate_total(item)

    if order.customer_type == CustomerTypeEnum.VIP:
        return total * 0.95
    if order.customer_type == CustomerTypeEnum.CORPORATIVE:
        return total * 0.90
    return total


def calculate_item_total(item: OrderItem) -> float:
    strategy = strategy_for_discount_type(item.discount_type)
    return strategy.calculate_total(item)