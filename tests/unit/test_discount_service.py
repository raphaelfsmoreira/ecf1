import pytest

from src.models.enums import DiscountType
from src.models.order_item import OrderItem
from src.services.discount_service import DiscountService
from src.strategies.item_discount_strategy import ItemDiscountStrategy
from src.strategies.volume_discount_strategy import VolumeDiscountStrategy


def test_volume_discount_strategy_aplica_15_porcento_para_tres_ou_mais_unidades():
    item = OrderItem(
        product_name='produto1',
        unit_price=100.0,
        quantity=3,
        discount_type=DiscountType.NORMAL,
    )

    total = DiscountService([VolumeDiscountStrategy()]).calculate_item_total(item)

    assert total == pytest.approx(255.0)


def test_volume_discount_strategy_nao_aplica_para_menos_de_tres_unidades():
    item = OrderItem(
        product_name='produto1',
        unit_price=100.0,
        quantity=2,
        discount_type=DiscountType.NORMAL,
    )

    total = DiscountService([VolumeDiscountStrategy()]).calculate_item_total(item)

    assert total == pytest.approx(200.0)


def test_discount_service_combina_desconto_do_item_com_desconto_por_volume():
    item = OrderItem(
        product_name='produto2',
        unit_price=100.0,
        quantity=3,
        discount_type=DiscountType.DISCOUNT_10,
    )

    total = DiscountService([
        ItemDiscountStrategy(),
        VolumeDiscountStrategy(),
    ]).calculate_item_total(item)

    assert total == pytest.approx(229.5)
