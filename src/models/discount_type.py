from enum import Enum

class DiscountType(Enum):
    NORMAL = "normal"
    DISCOUNT_10 = "desc10"
    DISCOUNT_20 = "desc20"
    FREE_SHIPPING = "frete_gratis"