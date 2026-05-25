from datetime import datetime

from src.models.enums import CustomerType, DiscountType, OrderStatus
from src.models.order import Order
from src.models.order_item import OrderItem
from src.repositories.order_repository_interface import OrderRepositoryInterface
from src.services.payment_service import PaymentService
from src.strategies.payment_strategy import PaymentStrategy


class InMemoryOrderRepository(OrderRepositoryInterface):
    def __init__(self) -> None:
        self.updated_status: tuple[int, OrderStatus] | None = None

    def add_order(self, order: Order) -> int:
        return 1

    def get_order_by_id(self, order_id: int) -> Order | None:
        return None

    def update_status(self, order_id: int, status: OrderStatus) -> None:
        self.updated_status = (order_id, status)

    def calculate_total_amount_by_customer_name(self, customer_name: str) -> float:
        return 0.0

    def cancel_order(self, order_id: int) -> None:
        self.updated_status = (order_id, OrderStatus.CANCELLED)


class AlwaysApprovePaymentStrategy(PaymentStrategy):
    def process_payment(self, order: Order, amount_paid: float) -> bool:
        return True


class AlwaysRejectPaymentStrategy(PaymentStrategy):
    def process_payment(self, order: Order, amount_paid: float) -> bool:
        return False


def make_order() -> Order:
    return Order(
        customer_name="Joao Silva",
        items=[OrderItem("produto1", 100.0, 1, DiscountType.NORMAL)],
        total_amount=100.0,
        status=OrderStatus.PENDING,
        created_at=datetime(2026, 5, 22, 12, 0, 0),
        customer_type=CustomerType.NORMAL,
    )


def test_payment_service_approves_order_when_strategy_accepts() -> None:
    repository = InMemoryOrderRepository()
    service = PaymentService(repository)

    result = service.process_payment(7, make_order(), 100.0, AlwaysApprovePaymentStrategy())

    assert result is True
    assert repository.updated_status == (7, OrderStatus.APPROVED)


def test_payment_service_does_not_update_status_when_strategy_rejects() -> None:
    repository = InMemoryOrderRepository()
    service = PaymentService(repository)

    result = service.process_payment(7, make_order(), 99.0, AlwaysRejectPaymentStrategy())

    assert result is False
    assert repository.updated_status is None