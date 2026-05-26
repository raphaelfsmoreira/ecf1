from src.models.order import Order
from src.services.payment_processor import PaymentProcessor


class CardPaymentProcessor(PaymentProcessor):
    def process(self, order: Order, paid_amount: float) -> bool:
        return paid_amount >= order.total_amount

    def approves_immediately(self) -> bool:
        return True


class PixPaymentProcessor(PaymentProcessor):
    def process(self, order: Order, paid_amount: float) -> bool:
        return paid_amount >= order.total_amount

    def approves_immediately(self) -> bool:
        return True


class BoletoPaymentProcessor(PaymentProcessor):
    def process(self, order: Order, paid_amount: float) -> bool:
        return paid_amount >= order.total_amount

    def approves_immediately(self) -> bool:
        return False


class CryptoPaymentProcessor(PaymentProcessor):
    FEE_RATE = 0.02

    def process(self, order: Order, paid_amount: float) -> bool:
        total_with_fee = order.total_amount * (1 + self.FEE_RATE)
        return paid_amount >= total_with_fee

    def approves_immediately(self) -> bool:
        return True