from datetime import datetime

from src.models.enums import CustomerType, DiscountType, OrderStatus, PaymentType
from src.models.order import Order
from src.models.order_item import OrderItem
from src.services.order_pricing_service import calculate_item_total, calculate_order_total
from src.strategies.discount_strategy import (
    NoDiscountStrategy,
    ProgressiveVolumeDiscountStrategy,
    TenPercentDiscountStrategy,
    TwentyPercentDiscountStrategy,
    strategy_for_discount_type,
)
from src.strategies.payment_strategy import (
    BoletoPaymentStrategy,
    CreditCardPaymentStrategy,
    CryptoPaymentStrategy,
    PixPaymentStrategy,
    strategy_for_payment_type,
)


def make_order(total_amount: float, customer_type: CustomerType = CustomerType.NORMAL) -> Order:
    return Order(
        customer_name="Test Customer",
        items=[],
        total_amount=total_amount,
        status=OrderStatus.PENDING,
        created_at=datetime(2026, 5, 22, 12, 0, 0),
        customer_type=customer_type,
    )


def test_discount_strategy_map_returns_expected_strategy() -> None:
    assert isinstance(strategy_for_discount_type(DiscountType.NORMAL), NoDiscountStrategy)
    assert isinstance(strategy_for_discount_type(DiscountType.DISCOUNT_10), TenPercentDiscountStrategy)
    assert isinstance(strategy_for_discount_type(DiscountType.DISCOUNT_20), TwentyPercentDiscountStrategy)


def test_progressive_volume_discount_applies_only_at_three_units() -> None:
    strategy = ProgressiveVolumeDiscountStrategy()

    small_item = OrderItem("product", 100.0, 2, DiscountType.NORMAL)
    bulk_item = OrderItem("product", 100.0, 3, DiscountType.NORMAL)

    assert strategy.calculate_total(small_item) == 200.0
    assert strategy.calculate_total(bulk_item) == 255.0


def test_order_pricing_service_matches_legacy_discounts() -> None:
    order = Order(
        customer_name="Joao Silva",
        items=[
            OrderItem("produto1", 100.0, 2, DiscountType.NORMAL),
            OrderItem("produto2", 50.0, 1, DiscountType.DISCOUNT_10),
        ],
        total_amount=0.0,
        status=OrderStatus.PENDING,
        created_at=datetime(2026, 5, 22, 12, 0, 0),
        customer_type=CustomerType.NORMAL,
    )

    assert calculate_item_total(order.items[0]) == 200.0
    assert calculate_item_total(order.items[1]) == 45.0
    assert calculate_order_total(order) == 245.0


def test_order_pricing_service_applies_customer_discount() -> None:
    order = Order(
        customer_name="Maria Santos",
        items=[OrderItem("produto3", 200.0, 1, DiscountType.DISCOUNT_20)],
        total_amount=0.0,
        status=OrderStatus.PENDING,
        created_at=datetime(2026, 5, 22, 12, 0, 0),
        customer_type=CustomerType.VIP,
    )

    assert calculate_order_total(order) == 152.0


def test_payment_strategy_map_returns_expected_strategy() -> None:
    assert isinstance(strategy_for_payment_type(PaymentType.CreditCard), CreditCardPaymentStrategy)
    assert isinstance(strategy_for_payment_type(PaymentType.Pix), PixPaymentStrategy)
    assert isinstance(strategy_for_payment_type(PaymentType.Boleto), BoletoPaymentStrategy)
    assert isinstance(strategy_for_payment_type(PaymentType.Crypto), CryptoPaymentStrategy)


def test_crypto_payment_requires_fee_buffer() -> None:
    order = make_order(100.0)
    strategy = CryptoPaymentStrategy()

    assert strategy.process_payment(order, 101.0) is False
    assert strategy.process_payment(order, 102.0) is True