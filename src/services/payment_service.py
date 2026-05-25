from abc import ABC, abstractmethod

from src.models.enums import OrderStatus
from src.models.order import Order
from src.repositories.order_repository_interface import OrderRepositoryInterface
from src.strategies.payment_strategy import PaymentStrategy


class PaymentServiceInterface(ABC):
    @abstractmethod
    def process_payment(
        self,
        order_id: int,
        order: Order,
        amount_paid: float,
        strategy: PaymentStrategy,
    ) -> bool:
        raise NotImplementedError


class PaymentService(PaymentServiceInterface):
    def __init__(self, repository: OrderRepositoryInterface) -> None:
        self._repository = repository

    def process_payment(
        self,
        order_id: int,
        order: Order,
        amount_paid: float,
        strategy: PaymentStrategy,
    ) -> bool:
        if not strategy.process_payment(order, amount_paid):
            return False

        self._repository.update_status(order_id, OrderStatus.APPROVED)
        return True