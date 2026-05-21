import pytest
from unittest.mock import MagicMock

from src.factories.order_factory import CorporateOrderFactory, NormalOrderFactory, VipOrderFactory
from src.models.enums import CustomerType, DiscountType, OrderStatus
from src.models.order import Order
from src.models.order_item import OrderItem
from src.services.order_service import OrderService


@pytest.fixture
def mock_repository():
    repo = MagicMock()
    repo.add_order.return_value = 1
    return repo


@pytest.fixture
def single_normal_item() -> list[OrderItem]:
    return [OrderItem(
        product_name='produto1',
        unit_price=100.0,
        quantity=1,
        discount_type=DiscountType.NORMAL,
    )]


def test_order_service_retorna_id_do_repositorio(mock_repository, single_normal_item):
    service = OrderService(repository=mock_repository, factory=NormalOrderFactory())

    order_id = service.create_order('Joao Silva', single_normal_item)

    assert order_id == 1
    mock_repository.add_order.assert_called_once()


def test_order_service_normal_persiste_order_com_total_correto(mock_repository):
    item1 = OrderItem(product_name='produto1', unit_price=100.0, quantity=2, discount_type=DiscountType.NORMAL)
    item2 = OrderItem(product_name='produto2', unit_price=50.0, quantity=1, discount_type=DiscountType.DISCOUNT_10)
    service = OrderService(repository=mock_repository, factory=NormalOrderFactory())

    service.create_order('Joao Silva', [item1, item2])

    persisted = mock_repository.add_order.call_args[0][0]
    assert persisted.total_amount == pytest.approx(245.0)
    assert persisted.customer_type == CustomerType.NORMAL
    assert persisted.status == OrderStatus.PENDING


def test_order_service_vip_persiste_order_com_desconto_vip(mock_repository, single_normal_item):
    service = OrderService(repository=mock_repository, factory=VipOrderFactory())

    service.create_order('Maria VIP', single_normal_item)

    persisted = mock_repository.add_order.call_args[0][0]
    assert persisted.total_amount == pytest.approx(95.0)
    assert persisted.customer_type == CustomerType.VIP


def test_order_service_corporativo_persiste_order_com_desconto_corporativo(mock_repository):
    item = OrderItem(product_name='produto1', unit_price=100.0, quantity=5, discount_type=DiscountType.NORMAL)
    service = OrderService(repository=mock_repository, factory=CorporateOrderFactory())

    service.create_order('Empresa XYZ', [item])

    persisted = mock_repository.add_order.call_args[0][0]
    assert persisted.total_amount == pytest.approx(450.0)
    assert persisted.customer_type == CustomerType.CORPORATIVE


def test_order_service_delega_criacao_para_factory(mock_repository, single_normal_item):
    mock_factory = MagicMock()
    mock_factory.create_order.return_value = MagicMock(spec=Order)
    service = OrderService(repository=mock_repository, factory=mock_factory)

    service.create_order('Joao', single_normal_item)

    mock_factory.create_order.assert_called_once_with('Joao', single_normal_item)
