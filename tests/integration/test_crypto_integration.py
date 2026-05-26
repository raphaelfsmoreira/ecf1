from src.factories.order_factory import NormalOrderFactory
from src.models.enums import DiscountType, PaymentType, OrderStatus
from src.models.order_item import OrderItem
from src.repositories.sqlite_order_repository import SqliteOrderRepository
from src.services.payment_processor_factory import PaymentProcessorFactory
from src.services.order_service import OrderService


def test_crypto_payment_integration(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    repo = SqliteOrderRepository(db_path='test_loja.db')

    # create order and persist
    item = OrderItem(
        product_name='produto_crypto',
        unit_price=100.0,
        quantity=1,
        discount_type=DiscountType.NORMAL,
    )

    order = NormalOrderFactory().create_order('Cliente Crypto', [item])
    order_id = repo.add_order(order)

    service = OrderService(repository=repo, factory=NormalOrderFactory(), payment_processor_factory=PaymentProcessorFactory())

    # process crypto payment equal to total
    result = service.process_payment(order_id=order_id, payment_type=PaymentType.Crypto, paid_amount=order.total_amount)

    assert result is True

    persisted = repo.get_order_by_id(order_id)
    assert persisted.status == OrderStatus.APPROVED
    assert persisted.payment_type == PaymentType.Crypto

    repo.close()
