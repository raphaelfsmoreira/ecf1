from datetime import datetime

from src.factories.order_factory import DefaultOrderFactory
from src.models.enums import CustomerType, DiscountType, OrderStatus
from src.models.order_item import OrderItem


def test_default_order_factory_creates_order_with_calculated_total() -> None:
    factory = DefaultOrderFactory(now_provider=lambda: datetime(2026, 5, 22, 12, 0, 0))

    order = factory.create_order(
        customer_name="Joao Silva",
        items=[
            OrderItem("produto1", 100.0, 2, DiscountType.NORMAL),
            OrderItem("produto2", 50.0, 1, DiscountType.DISCOUNT_10),
        ],
        customer_type=CustomerType.NORMAL,
    )

    assert order.customer_name == "Joao Silva"
    assert order.total_amount == 245.0
    assert order.status == OrderStatus.PENDING
    assert order.created_at == datetime(2026, 5, 22, 12, 0, 0)
    assert order.customer_type == CustomerType.NORMAL