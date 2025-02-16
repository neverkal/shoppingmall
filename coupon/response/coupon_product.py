from typing import Optional
from pydantic import BaseModel


class CouponProduct(BaseModel):
    id: int
    name: str
    description: str
    price: int
    category: str
    discount_rate: float
    coupon_applicable: bool
    discounted_price: int
    final_price_with_coupon: Optional[int] = None