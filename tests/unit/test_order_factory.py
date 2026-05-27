import pytest

from src.factories.order_factory import (
    CorporateOrderFactory,
    NormalOrderFactory,
    VipOrderFactory,
    get_order_factory,
)
from src.models.enums import CustomerType, DiscountType, OrderStatus
from src.models.order_item import OrderItem


@pytest.fixture
def normal_item() -> OrderItem:
    return OrderItem(
        product_name='produto1',
        unit_price=100.0,
        quantity=2,
        discount_type=DiscountType.NORMAL,
    )


@pytest.fixture
def desc10_item() -> OrderItem:
    return OrderItem(
        product_name='produto2',
        unit_price=50.0,
        quantity=1,
        discount_type=DiscountType.DISCOUNT_10,
    )


@pytest.fixture
def desc20_item() -> OrderItem:
    return OrderItem(
        product_name='produto3',
        unit_price=200.0,
        quantity=1,
        discount_type=DiscountType.DISCOUNT_20,
    )


def test_normal_factory_calcula_total_mixed_discounts(normal_item: OrderItem, desc10_item: OrderItem):
    # produto1: 100*2=200, produto2: 50*1*0.9=45 => total=245
    order = NormalOrderFactory().create_order('Joao Silva', [normal_item, desc10_item])

    assert order.total_amount == pytest.approx(245.0)
    assert order.customer_type == CustomerType.NORMAL
    assert order.status == OrderStatus.PENDING
    assert order.customer_name == 'Joao Silva'


def test_normal_factory_item_frete_gratis_nao_aplica_desconto():
    item = OrderItem(
        product_name='produto1',
        unit_price=100.0,
        quantity=1,
        discount_type=DiscountType.FREE_SHIPPING,
    )
    order = NormalOrderFactory().create_order('Joao', [item])

    assert order.total_amount == pytest.approx(100.0)


def test_normal_factory_item_desc20(desc20_item: OrderItem):
    # produto3: 200*1*0.8=160
    order = NormalOrderFactory().create_order('Cliente', [desc20_item])

    assert order.total_amount == pytest.approx(160.0)


def test_vip_factory_aplica_5_porcento_sobre_total_dos_itens(normal_item: OrderItem):
    # produto1: 100*2=200, VIP 5%: 200*0.95=190
    order = VipOrderFactory().create_order('Maria VIP', [normal_item])

    assert order.total_amount == pytest.approx(190.0)
    assert order.customer_type == CustomerType.VIP


def test_vip_factory_aplica_desconto_vip_sobre_item_com_desc20(desc20_item: OrderItem):
    # produto3: 200*0.8=160, VIP 5%: 160*0.95=152
    order = VipOrderFactory().create_order('Maria Santos', [desc20_item])

    assert order.total_amount == pytest.approx(152.0)


def test_corporate_factory_aplica_10_porcento_sobre_total_dos_itens():
    item = OrderItem(
        product_name='produto1',
        unit_price=100.0,
        quantity=5,
        discount_type=DiscountType.NORMAL,
    )
    
    order = CorporateOrderFactory().create_order('Empresa XYZ', [item])

    assert order.total_amount == pytest.approx(382.5)
    assert order.customer_type == CustomerType.CORPORATIVE


def test_get_order_factory_retorna_normal_factory():
    assert isinstance(get_order_factory(CustomerType.NORMAL), NormalOrderFactory)


def test_get_order_factory_retorna_vip_factory():
    assert isinstance(get_order_factory(CustomerType.VIP), VipOrderFactory)


def test_get_order_factory_retorna_corporate_factory():
    assert isinstance(get_order_factory(CustomerType.CORPORATIVE), CorporateOrderFactory)


def test_get_order_factory_levanta_erro_para_tipo_invalido():
    with pytest.raises(ValueError):
        get_order_factory('tipo_invalido')
