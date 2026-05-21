from enum import Enum

class PaymentType(Enum):
    CreditCard = 'Cartão'
    Pix = 'Pix'
    Boleto = 'Boleto'
    Crypto = 'Criptomoeda'