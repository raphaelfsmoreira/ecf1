from src.models.enums import PaymentType
from src.services.payment_processor import PaymentProcessor
from src.services.payment_strategies import (
    BoletoPaymentProcessor,
    CardPaymentProcessor,
    CryptoPaymentProcessor,
    PixPaymentProcessor,
)


class PaymentProcessorFactory:
    def __init__(self) -> None:
        self._processors: dict[PaymentType, PaymentProcessor] = {
            PaymentType.CreditCard: CardPaymentProcessor(),
            PaymentType.Pix: PixPaymentProcessor(),
            PaymentType.Boleto: BoletoPaymentProcessor(),
            PaymentType.Crypto: CryptoPaymentProcessor(),
        }

    def get_processor(self, payment_type: PaymentType) -> PaymentProcessor:
        processor = self._processors.get(payment_type)
        if processor is None:
            raise ValueError(f'No payment processor registered for payment type: {payment_type}')
        return processor
