from decimal import Decimal
from typing import Optional

from django.db import models

from category.models import Category
from coupon.models import Coupon


class Product(models.Model):
    id: int = models.BigAutoField(primary_key=True)
    name: str = models.CharField(max_length=255)
    description: str = models.TextField()
    price: int = models.IntegerField()
    category: "Category" = models.ForeignKey('category.Category', on_delete=models.CASCADE, related_name='products')
    discount_rate: float = models.FloatField(default=0.0)
    coupon_applicable: bool = models.BooleanField(default=False)

    def calculate_discounted_price(self) -> int:
        """할인율을 적용한 가격 계산"""
        discounted_price = self.price * (1 - self.discount_rate)
        return int(discounted_price)

    def calculate_final_price(self, coupon: Optional["Coupon"] = None):
        """최종 가격 계산 (쿠폰 적용 포함)"""
        final_price = self.calculate_discounted_price()
        if coupon and self.coupon_applicable:
            final_price *= (1 - coupon.discount_rate)
        return int(final_price)

    def __str__(self) -> str:
        return self.name