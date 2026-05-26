from src.factories.order_factory import NormalOrderFactory
from src.models.enums import DiscountType, PaymentType, OrderStatus
from src.models.order_item import OrderItem
from src.repositories.sqlite_order_repository import SqliteOrderRepository
from src.services.payment_processor_factory import PaymentProcessorFactory
from src.services.order_service import OrderService


from src.factories.order_factory import NormalOrderFactory
from src.models.enums import DiscountType, PaymentType, OrderStatus
from src.models.order_item import OrderItem
from src.repositories.sqlite_order_repository import SqliteOrderRepository
from src.services.payment_processor_factory import PaymentProcessorFactory
from src.services.order_service import OrderService


def test_crypto_payment_requires_two_percent_fee(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    repo = SqliteOrderRepository(db_path='test_loja.db')

    item = OrderItem(
        product_name='produto_crypto',
        unit_price=100.0,
        quantity=1,
        discount_type=DiscountType.NORMAL,
    )

    order = NormalOrderFactory().create_order('Cliente Crypto', [item])
    order_id = repo.add_order(order)

    service = OrderService(
        repository=repo,
        factory=NormalOrderFactory(),
        payment_processor_factory=PaymentProcessorFactory(),
    )

    result = service.process_payment(
        order_id=order_id,
        payment_type=PaymentType.Crypto,
        paid_amount=order.total_amount,
    )

    assert result is False

    persisted = repo.get_order_by_id(order_id)
    assert persisted.status == OrderStatus.PENDING
    assert persisted.payment_type == PaymentType.Crypto

    repo.close()


def test_crypto_payment_approves_when_two_percent_fee_is_paid(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    repo = SqliteOrderRepository(db_path='test_loja.db')

    item = OrderItem(
        product_name='produto_crypto',
        unit_price=100.0,
        quantity=1,
        discount_type=DiscountType.NORMAL,
    )

    order = NormalOrderFactory().create_order('Cliente Crypto', [item])
    order_id = repo.add_order(order)

    service = OrderService(
        repository=repo,
        factory=NormalOrderFactory(),
        payment_processor_factory=PaymentProcessorFactory(),
    )

    result = service.process_payment(
        order_id=order_id,
        payment_type=PaymentType.Crypto,
        paid_amount=order.total_amount * 1.02,
    )

    assert result is True

    persisted = repo.get_order_by_id(order_id)
    assert persisted.status == OrderStatus.APPROVED
    assert persisted.payment_type == PaymentType.Crypto

    repo.close()
