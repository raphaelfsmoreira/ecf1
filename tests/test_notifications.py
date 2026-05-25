from datetime import datetime

from src.models.enums import CustomerType, OrderStatus
from src.models.order import Order
from src.observers.order_notification_observers import (
    AccountManagerNotificationObserver,
    EmailNotificationObserver,
    OrderNotificationPublisher,
    SmsNotificationObserver,
    WhatsAppNotificationObserver,
)


def make_order(customer_name: str, customer_type: CustomerType) -> Order:
    return Order(
        customer_name=customer_name,
        items=[],
        total_amount=100.0,
        status=OrderStatus.PENDING,
        created_at=datetime(2026, 5, 22, 12, 0, 0),
        customer_type=customer_type,
    )


def test_normal_customer_receives_email_and_whatsapp(capsys) -> None:
    publisher = OrderNotificationPublisher()
    publisher.subscribe(EmailNotificationObserver())
    publisher.subscribe(SmsNotificationObserver())
    publisher.subscribe(AccountManagerNotificationObserver())
    publisher.subscribe(WhatsAppNotificationObserver())

    publisher.publish(make_order("Joao Silva", CustomerType.NORMAL))

    output = capsys.readouterr().out

    assert "Email enviado para Joao Silva: Pedido recebido!" in output
    assert "WhatsApp enviado para Joao Silva: Pedido recebido!" in output
    assert "SMS enviado" not in output
    assert "gerente de conta" not in output


def test_vip_customer_receives_email_sms_and_whatsapp(capsys) -> None:
    publisher = OrderNotificationPublisher()
    publisher.subscribe(EmailNotificationObserver())
    publisher.subscribe(SmsNotificationObserver())
    publisher.subscribe(WhatsAppNotificationObserver())

    publisher.publish(make_order("Maria Santos", CustomerType.VIP))

    output = capsys.readouterr().out

    assert "Email enviado para Maria Santos: Pedido recebido!" in output
    assert "SMS enviado para Maria Santos: Pedido VIP recebido!" in output
    assert "WhatsApp enviado para Maria Santos: Pedido recebido!" in output


def test_corporate_customer_receives_email_manager_and_whatsapp(capsys) -> None:
    publisher = OrderNotificationPublisher()
    publisher.subscribe(EmailNotificationObserver())
    publisher.subscribe(AccountManagerNotificationObserver())
    publisher.subscribe(WhatsAppNotificationObserver())

    publisher.publish(make_order("Empresa XYZ", CustomerType.CORPORATIVE))

    output = capsys.readouterr().out

    assert "Email enviado para Empresa XYZ: Pedido recebido!" in output
    assert "Notificação enviada ao gerente de conta de Empresa XYZ" in output
    assert "WhatsApp enviado para Empresa XYZ: Pedido recebido!" in output