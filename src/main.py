from src.database.database import SQLiteDatabase
from src.database.schema import create_tables

from src.models.enums import (
    CustomerType,
    DiscountType,
    PaymentType,
)

from src.models.order_item import OrderItem

from src.repositories.order_repository import OrderRepository

from src.factories.order_factory import get_order_factory
from src.factories.payment_processor_factory import (
    PaymentProcessorFactory,
)

from src.services.order_service import OrderService


def main() -> None:
    print('=== LOJA VERDE ===')

    # Banco
    database = SQLiteDatabase()
    create_tables(database)

    # Repository
    repository = OrderRepository(database)

    # Factories
    order_factory = get_order_factory(
        CustomerType.VIP
    )

    payment_factory = PaymentProcessorFactory()

    # Service principal
    order_service = OrderService(
        repository=repository,
        factory=order_factory,
        payment_processor_factory=payment_factory,
    )

    # Pedido exemplo
    items = [
        OrderItem(
            product_name='produto1',
            unit_price=100.0,
            quantity=3,
            discount_type=DiscountType.NORMAL,
        ),
        OrderItem(
            product_name='produto2',
            unit_price=50.0,
            quantity=1,
            discount_type=DiscountType.DISCOUNT_10,
        ),
    ]

    # Criação do pedido
    order_id = order_service.create_order(
        customer_name='Joao Silva',
        items=items,
    )

    print(f'Pedido criado com ID {order_id}')

    # Pagamento em criptomoeda
    payment_success = order_service.process_payment(
        order_id=order_id,
        payment_type=PaymentType.Crypto,
        paid_amount=350.0,
    )

    if payment_success:
        print('Pagamento aprovado!')
    else:
        print('Pagamento recusado!')

    database.close()


if __name__ == '__main__':
    main()