import json
from datetime import datetime

from src.repositories.order_repository_interface import OrderRepositoryInterface

from src.database.database import SQLiteDatabase

from src.models.order import Order
from src.models.order_item import OrderItem
from src.models.enums import CustomerType, DiscountType, OrderStatus, PaymentType


# Nada como criar um ORM na mão...

class OrderRepository(OrderRepositoryInterface):

    def __init__(self, db: SQLiteDatabase) -> None:
        self.db = db

    def add_order(self, order: Order) -> int:

        items_dict = [
            {
                "product_name": item.product_name,
                "unit_price": item.unit_price,
                "quantity": item.quantity,
                "discount_type": item.discount_type.value
            }
            for item in order.items
        ]

        self.db.execute(
            '''
            INSERT INTO orders (
                customer_name,
                items,
                total_amount,
                status,
                created_at,
                customer_type
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                order.customer_name,
                json.dumps(items_dict),
                order.total_amount,
                order.status.value,
                order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                order.customer_type.value
            )
        )

        self.db.commit()

        return int(self.db.lastrowid())

    def get_order_by_id(self, order_id: int) -> Order | None:

        # O ideal não é usar * e sim explicitar a ordem das colunas.

        self.db.execute('''
            SELECT  id, 
                    customer_name, 
                    items, 
                    total_amount, 
                    status, 
                    created_at, 
                    customer_type
            FROM orders
            WHERE id = ?
            ''', (order_id,),
        )

        row = self.db.fetchone()

        # Se não existe um pedido com esse id, retorne None.
        if not row:
            return None

        # Não se deve retornar a tupla de elementos do banco de dados, mas sim
        # o objeto Order já construído bonitinho. :)

        # Antes de mais nada, precisamos transformar os itens serializados do banco para objetos
        # do tipo OrderItem

        # Carrega a string do banco como uma lista de dicionários puros
        raw_items = json.loads(row[2])

        # Converte explicitamente cada dicionário em um objeto OrderItem real
        order_items = [
            OrderItem(
                product_name=item['product_name'],
                unit_price=float(item['unit_price']),
                quantity=int(item['quantity']),
                discount_type=DiscountType(item['discount_type'])  # Converte a string de volta para o Enum
            )
            for item in raw_items
        ]

        return Order(
            id=row[0],
            customer_name=row[1],
            items=order_items,
            total_amount=row[3],
            status=OrderStatus(row[4]),
            created_at=datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S"),
            customer_type=CustomerType(row[6])
        )

    def update_status(self, order_id: int, status: OrderStatus) -> None:

        # A lógica de enviar Sms, etc não entra aqui.
        # Aqui só se faz as ações no banco.
        # As classes responsaveis por enviar mensagem (MessageService, etc.) é quem chama esse metodo...

        self.db.execute(
            '''
            UPDATE orders
            SET status = ?
            WHERE id = ?
            ''',
            (
                status.value, # Não passar o objeto Enum e sim seu valor!
                order_id
            )
        )

        self.db.commit()

    def calculate_total_amount_by_customer_name(self, customer_name: str) -> float:

        # Delegar para o db fazer a soma
        self.db.execute(
            '''
            SELECT SUM(total_amount)
            FROM orders
            WHERE customer_name = ?
            ''',
            (customer_name,)
        )

        result = self.db.fetchone()

        # Se o cliente não existir, retorna zero
        if result is None or result[0] is None:
            return 0.0

        return float(result[0])


    # Aqui reaproveitamos o metodo update status...
    # Lembrar que enviar a mensagem é responsabilidade de um service, e não do repository
    def cancel_order(self, order_id: int) -> None:

        self.update_status(order_id, OrderStatus.CANCELLED)

    def update_payment_type(
            self,
            order_id: int,
            payment_type: PaymentType,
    ) -> None:

        self.db.execute(
            '''
            UPDATE orders
            SET payment_type = ?
            WHERE id = ?
            ''',
            (
                payment_type.value,
                order_id,
            )
        )

        self.db.commit()
