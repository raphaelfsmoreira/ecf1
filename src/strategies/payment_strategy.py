from abc import ABC, abstractmethod

from src.models.enums import PaymentType
from src.models.order import Order


class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, order: Order, amount_paid: float) -> bool:
        raise NotImplementedError


class CreditCardPaymentStrategy(PaymentStrategy):
    def process_payment(self, order: Order, amount_paid: float) -> bool:
        return amount_paid >= order.total_amount


class PixPaymentStrategy(PaymentStrategy):
    def process_payment(self, order: Order, amount_paid: float) -> bool:
        return amount_paid >= order.total_amount


class BoletoPaymentStrategy(PaymentStrategy):
    def process_payment(self, order: Order, amount_paid: float) -> bool:
        return amount_paid >= order.total_amount


class CryptoPaymentStrategy(PaymentStrategy):
    def process_payment(self, order: Order, amount_paid: float) -> bool:
        amount_with_fee = order.total_amount * 1.02
        return amount_paid >= amount_with_fee


def strategy_for_payment_type(payment_type: PaymentType) -> PaymentStrategy:
    if payment_type is PaymentType.CreditCard:
        return CreditCardPaymentStrategy()
    if payment_type is PaymentType.Pix:
        return PixPaymentStrategy()
    if payment_type is PaymentType.Boleto:
        return BoletoPaymentStrategy()
    return CryptoPaymentStrategy()
