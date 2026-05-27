import json
import sqlite3
from datetime import datetime

from src.models.enums import CustomerType, DiscountType, OrderStatus, PaymentType
from src.models.order import Order
from src.models.order_item import OrderItem
from src.repositories.order_repository_interface import OrderRepositoryInterface


class SqliteOrderRepository(OrderRepositoryInterface):
    def __init__(self, db_path: str = 'loja.db') -> None:
        self._db = sqlite3.connect(db_path)
        self._cursor = self._db.cursor()
        self._cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS ped(
                id INTEGER PRIMARY KEY,
                cli TEXT,
                itens TEXT,
                tot REAL,
                st TEXT,
                dt TEXT,
                tp TEXT,
                payment_type TEXT
            )
            '''
        )
        self._db.commit()

    def add_order(self, order: Order) -> int:
        serialized_items = json.dumps(
            [
                {
                    'nome': item.product_name,
                    'p': item.unit_price,
                    'q': item.quantity,
                    'tipo': item.discount_type.value,
                }
                for item in order.items
            ]
        )
        created_at = order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        payment_type = order.payment_type.value if order.payment_type else None

        self._cursor.execute(
            '''
            INSERT INTO ped (cli, itens, tot, st, dt, tp, payment_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                order.customer_name,
                serialized_items,
                order.total_amount,
                order.status.value,
                created_at,
                order.customer_type.value,
                payment_type,
            ),
        )
        self._db.commit()
        last = self._cursor.lastrowid
        return int(last) if last is not None else 0

    def get_order_by_id(self, order_id: int) -> Order | None:
        self._cursor.execute(
            'SELECT id, cli, itens, tot, st, dt, tp, payment_type FROM ped WHERE id=?',
            (order_id,),
        )
        row = self._cursor.fetchone()
        if row is None:
            return None

        order_items = [
            OrderItem(
                product_name=item['nome'],
                unit_price=float(item['p']),
                quantity=int(item['q']),
                discount_type=DiscountType(item['tipo']),
            )
            for item in json.loads(row[2])
        ]

        payment_type = PaymentType(row[7]) if row[7] else None

        return Order(
            id=int(row[0]),
            customer_name=row[1],
            items=order_items,
            total_amount=float(row[3]),
            status=OrderStatus(row[4]),
            created_at=datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S'),
            customer_type=CustomerType(row[6]),
            payment_type=payment_type,
        )

    def update_status(self, order_id: int, status: OrderStatus) -> None:
        self._cursor.execute('UPDATE ped SET st=? WHERE id=?', (status.value, order_id))
        self._db.commit()

    def update_payment_type(self, order_id: int, payment_type: PaymentType) -> None:
        self._cursor.execute('UPDATE ped SET payment_type=? WHERE id=?', (payment_type.value, order_id))
        self._db.commit()

    def calculate_total_amount_by_customer_name(self, customer_name: str) -> float:
        self._cursor.execute('SELECT tot FROM ped WHERE cli=?', (customer_name,))
        rows = self._cursor.fetchall()
        return sum(float(row[0]) for row in rows)

    def cancel_order(self, order_id: int) -> None:
        self.update_status(order_id, OrderStatus.CANCELLED)

    def close(self) -> None:
        self._db.close()
