from src.factories.order_factory import NormalOrderFactory
from src.models.enums import DiscountType, PaymentType
from src.models.order_item import OrderItem
from src.repositories.sqlite_order_repository import SqliteOrderRepository
from src.services.notification_service import create_default_notification_service
from src.services.order_service import OrderService
from src.factories.payment_processor_factory import PaymentProcessorFactory


def test_order_service_notifica_whatsapp_ao_criar_pedido(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    repo = SqliteOrderRepository(db_path='test_loja.db')
    service = OrderService(
        repository=repo,
        factory=NormalOrderFactory(),
        notification_service=create_default_notification_service(),
    )
    item = OrderItem('produto1', 100.0, 1, DiscountType.NORMAL)

    service.create_order('Cliente WhatsApp', [item])

    output = capsys.readouterr().out
    assert 'WhatsApp enviado para Cliente WhatsApp: Pedido recebido!' in output
    repo.close()


def test_order_service_notifica_whatsapp_ao_aprovar_pagamento(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    repo = SqliteOrderRepository(db_path='test_loja.db')
    item = OrderItem('produto1', 100.0, 1, DiscountType.NORMAL)
    order_id = repo.add_order(NormalOrderFactory().create_order('Cliente WhatsApp', [item]))
    service = OrderService(
        repository=repo,
        factory=NormalOrderFactory(),
        payment_processor_factory=PaymentProcessorFactory(),
        notification_service=create_default_notification_service(),
    )

    service.process_payment(order_id, PaymentType.Pix, 100.0)

    output = capsys.readouterr().out
    assert 'WhatsApp enviado para Cliente WhatsApp: Pedido aprovado!' in output
    repo.close()
