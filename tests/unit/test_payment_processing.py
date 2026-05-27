import pytest

from src.models.order import Order


@pytest.fixture
def sample_order() -> Order:
    return Order(
        id=10,
        customer_name='Cliente Teste',
        items=[
            OrderItem(
                product_name='produto1',
                unit_price=100.0,
                quantity=1,
                discount_type=DiscountType.NORMAL,
            )
        ],
        total_amount=100.0,
        status=OrderStatus.PENDING,
        created_at=datetime.now(),
        customer_type=CustomerType.NORMAL,
    )


@pytest.fixture
def mock_repository(sample_order: Order):
    repo = MagicMock()
    repo.get_order_by_id.return_value = sample_order
    repo.add_order.return_value = sample_order.id
    return repo


def test_payment_processor_factory_retorna_crypto_processor():
    processor = PaymentProcessorFactory().get_processor(PaymentType.Crypto)
    assert processor.approves_immediately() is True


def test_payment_processor_factory_erro_para_tipo_invalido():
    with pytest.raises(ValueError):
        PaymentProcessorFactory().get_processor('invalido')


def test_order_service_pagamento_cartao_aprova(mock_repository):
    service = OrderService(
        repository=mock_repository,
        factory=MagicMock(),
        payment_processor_factory=PaymentProcessorFactory(),
    )

    result = service.process_payment(order_id=10, payment_type=PaymentType.CreditCard, paid_amount=100.0)

    assert result is True
    mock_repository.update_payment_type.assert_called_once_with(10, PaymentType.CreditCard)
    mock_repository.update_status.assert_called_once_with(10, OrderStatus.APPROVED)


def test_order_service_pagamento_boleto_nao_aprova(mock_repository):
    service = OrderService(
        repository=mock_repository,
        factory=MagicMock(),
        payment_processor_factory=PaymentProcessorFactory(),
    )

    result = service.process_payment(order_id=10, payment_type=PaymentType.Boleto, paid_amount=100.0)

    assert result is True
    mock_repository.update_payment_type.assert_called_once_with(10, PaymentType.Boleto)
    mock_repository.update_status.assert_not_called()


def test_order_service_pagamento_insuficiente_falha(mock_repository):
    service = OrderService(
        repository=mock_repository,
        factory=MagicMock(),
        payment_processor_factory=PaymentProcessorFactory(),
    )

    result = service.process_payment(order_id=10, payment_type=PaymentType.Pix, paid_amount=99.0)

    assert result is False
    mock_repository.update_payment_type.assert_called_once_with(10, PaymentType.Pix)
    mock_repository.update_status.assert_not_called()


def test_order_service_pagamento_crypto_aprova(mock_repository):
    service = OrderService(
        repository=mock_repository,
        factory=MagicMock(),
        payment_processor_factory=PaymentProcessorFactory(),
    )

    result = service.process_payment(order_id=10, payment_type=PaymentType.Crypto, paid_amount=100.0)

    assert result is True
    mock_repository.update_payment_type.assert_called_once_with(10, PaymentType.Crypto)
    mock_repository.update_status.assert_called_once_with(10, OrderStatus.APPROVED)


def test_order_service_pagamento_pedido_inexistente_retorna_false(mock_repository):
    mock_repository.get_order_by_id.return_value = None
    service = OrderService(
        repository=mock_repository,
        factory=MagicMock(),
        payment_processor_factory=PaymentProcessorFactory(),
    )

    result = service.process_payment(order_id=999, payment_type=PaymentType.Pix, paid_amount=100.0)

    assert result is False
    mock_repository.update_payment_type.assert_not_called()
    mock_repository.update_status.assert_not_called()
from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.models.enums import CustomerType, DiscountType, OrderStatus, PaymentType
from src.models.order import Order
from src.models.order_item import OrderItem
from src.services.order_service import OrderService
from src.factories.payment_processor_factory import PaymentProcessorFactory


@pytest.fixture
def sample_order() -> Order:
    return Order(
        id=10,
        customer_name='Cliente Teste',
        items=[
            OrderItem(
                product_name='produto1',
                unit_price=100.0,
                quantity=1,
                discount_type=DiscountType.NORMAL,
            )
        ],
        total_amount=100.0,
        status=OrderStatus.PENDING,
        created_at=datetime.now(),
        customer_type=CustomerType.NORMAL,
    )


@pytest.fixture
def mock_repository(sample_order: Order):
    repo = MagicMock()
    repo.get_order_by_id.return_value = sample_order
    repo.add_order.return_value = sample_order.id
    return repo


def test_payment_processor_factory_retorna_crypto_processor():
    processor = PaymentProcessorFactory().get_processor(PaymentType.Crypto)
    assert processor.approves_immediately() is True


def test_payment_processor_factory_erro_para_tipo_invalido():
    with pytest.raises(ValueError):
        PaymentProcessorFactory().get_processor('invalido')


def test_order_service_pagamento_cartao_aprova(mock_repository):
    service = OrderService(
        repository=mock_repository,
        factory=MagicMock(),
        payment_processor_factory=PaymentProcessorFactory(),
    )

    result = service.process_payment(order_id=10, payment_type=PaymentType.CreditCard, paid_amount=100.0)

    assert result is True
    mock_repository.update_payment_type.assert_called_once_with(10, PaymentType.CreditCard)
    mock_repository.update_status.assert_called_once_with(10, OrderStatus.APPROVED)


def test_order_service_pagamento_boleto_nao_aprova(mock_repository):
    service = OrderService(
        repository=mock_repository,
        factory=MagicMock(),
        payment_processor_factory=PaymentProcessorFactory(),
    )

    result = service.process_payment(order_id=10, payment_type=PaymentType.Boleto, paid_amount=100.0)

    assert result is True
    mock_repository.update_payment_type.assert_called_once_with(10, PaymentType.Boleto)
    mock_repository.update_status.assert_not_called()


def test_order_service_pagamento_insuficiente_falha(mock_repository):
    service = OrderService(
        repository=mock_repository,
        factory=MagicMock(),
        payment_processor_factory=PaymentProcessorFactory(),
    )

    result = service.process_payment(order_id=10, payment_type=PaymentType.Pix, paid_amount=99.0)

    assert result is False
    mock_repository.update_payment_type.assert_called_once_with(10, PaymentType.Pix)
    mock_repository.update_status.assert_not_called()


def test_order_service_pagamento_crypto_exige_taxa_de_dois_por_cento(mock_repository):
    service = OrderService(
        repository=mock_repository,
        factory=MagicMock(),
        payment_processor_factory=PaymentProcessorFactory(),
    )

    result = service.process_payment(order_id=10, payment_type=PaymentType.Crypto, paid_amount=100.0)

    assert result is False
    mock_repository.update_payment_type.assert_called_once_with(10, PaymentType.Crypto)
    mock_repository.update_status.assert_not_called()


def test_order_service_pagamento_crypto_aprova_com_taxa_de_dois_por_cento(mock_repository):
    service = OrderService(
        repository=mock_repository,
        factory=MagicMock(),
        payment_processor_factory=PaymentProcessorFactory(),
    )

    result = service.process_payment(order_id=10, payment_type=PaymentType.Crypto, paid_amount=102.0)

    assert result is True
    mock_repository.update_payment_type.assert_called_once_with(10, PaymentType.Crypto)
    mock_repository.update_status.assert_called_once_with(10, OrderStatus.APPROVED)


def test_order_service_pagamento_pedido_inexistente_retorna_false(mock_repository):
    mock_repository.get_order_by_id.return_value = None
    service = OrderService(
        repository=mock_repository,
        factory=MagicMock(),
        payment_processor_factory=PaymentProcessorFactory(),
    )

    result = service.process_payment(order_id=999, payment_type=PaymentType.Pix, paid_amount=100.0)

    assert result is False
    mock_repository.update_payment_type.assert_not_called()
    mock_repository.update_status.assert_not_called()
