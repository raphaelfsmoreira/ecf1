from src.factories.order_factory import OrderFactory
from src.models.enums import OrderStatus, PaymentType
from src.repositories.order_repository_interface import OrderRepositoryInterface
from src.models.order_item import OrderItem
from src.services.payment_processor_factory import PaymentProcessorFactory
from src.factories.notification_factory import NotificationFactory
from src.services.notification_service import NotificationService


class OrderService:
    def __init__(
        self,
        repository: OrderRepositoryInterface,
        factory: OrderFactory,
        payment_processor_factory: PaymentProcessorFactory | None = None,
        notification_service: NotificationService | None = None,
        notification_factory: NotificationFactory | None = None,
    ) -> None:
        self._repository = repository
        self._factory = factory
        self._payment_processor_factory = payment_processor_factory
        self._notification_service = notification_service
        self._notification_factory = notification_factory or NotificationFactory()

    def create_order(self, customer_name: str, items: list[OrderItem]) -> int:
        order = self._factory.create_order(customer_name, items)
        order_id = self._repository.add_order(order)
        self._notify(order, 'Pedido recebido!')
        return order_id

    def process_payment(self, order_id: int, payment_type: PaymentType, paid_amount: float) -> bool:
        if self._payment_processor_factory is None:
            raise RuntimeError('Payment processor factory is not configured for OrderService')

        order = self._repository.get_order_by_id(order_id)
        if order is None:
            return False

        self._repository.update_payment_type(order_id, payment_type)
        order.payment_type = payment_type

        processor = self._payment_processor_factory.get_processor(payment_type)
        accepted = processor.process(order, paid_amount)
        if not accepted:
            return False

        if processor.approves_immediately():
            self._repository.update_status(order_id, OrderStatus.APPROVED)
            order.status = OrderStatus.APPROVED
            self._notify(order, 'Pedido aprovado!')

        return True

    def _notify(self, order, message: str) -> None:
        notification_service = self._notification_service
        if notification_service is None:
            notification_service = self._notification_factory.create_for_customer(order.customer_type)
        notification_service.notify(order, message)
