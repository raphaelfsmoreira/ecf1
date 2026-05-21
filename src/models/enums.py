from enum import Enum

class CustomerType(Enum):
    NORMAL = 'normal'
    VIP = 'vip'
    CORPORATIVE = 'corporativo'


class DiscountType(Enum):
    NORMAL = "normal"
    DISCOUNT_10 = "desc10"
    DISCOUNT_20 = "desc20"
    FREE_SHIPPING = "frete_gratis"


class OrderStatus(Enum):
    PENDING = "pendente"
    APPROVED = "aprovado"
    SENT = "enviado"
    DELIVERED = "entregue"
    CANCELLED = "cancelado"


class PaymentType(Enum):
    CreditCard = 'Cartão'
    Pix = 'Pix'
    Boleto = 'Boleto'
    Crypto = 'Criptomoeda'
