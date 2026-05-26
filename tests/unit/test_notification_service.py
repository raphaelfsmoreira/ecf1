from src.factories.order_factory import CorporateOrderFactory, NormalOrderFactory, VipOrderFactory
from src.models.enums import DiscountType
from src.models.order_item import OrderItem
from src.services.notification_service import create_default_notification_service


# Funcao para criacao de order padrao para ser incluido nos testes
def _single_item() -> list[OrderItem]:
    return [
        OrderItem(
            product_name='produto1',
            unit_price=100.0,
            quantity=1,
            discount_type=DiscountType.NORMAL,
        )
    ]


def test_notification_service_envia_email_e_whatsapp_para_cliente_normal(capsys):
    order = NormalOrderFactory().create_order('Joao Silva', _single_item())
    service = create_default_notification_service()

    service.notify(order, 'Pedido recebido!')

    output = capsys.readouterr().out
    assert 'Email enviado para Joao Silva: Pedido recebido!' in output
    assert 'WhatsApp enviado para Joao Silva: Pedido recebido!' in output
    assert 'SMS enviado' not in output
    assert 'gerente de conta' not in output


def test_notification_service_envia_sms_adicional_para_cliente_vip(capsys):
    order = VipOrderFactory().create_order('Maria Santos', _single_item())
    service = create_default_notification_service()

    service.notify(order, 'Pedido recebido!')

    output = capsys.readouterr().out
    assert 'Email enviado para Maria Santos: Pedido recebido!' in output
    assert 'WhatsApp enviado para Maria Santos: Pedido recebido!' in output
    assert 'SMS enviado para Maria Santos: Pedido recebido!' in output


def test_notification_service_notifica_gerente_para_cliente_corporativo(capsys):
    order = CorporateOrderFactory().create_order('Empresa XYZ', _single_item())
    service = create_default_notification_service()

    service.notify(order, 'Pedido recebido!')

    output = capsys.readouterr().out
    assert 'Email enviado para Empresa XYZ: Pedido recebido!' in output
    assert 'WhatsApp enviado para Empresa XYZ: Pedido recebido!' in output
    assert 'Notificação enviada ao gerente de conta de Empresa XYZ: Pedido recebido!' in output
