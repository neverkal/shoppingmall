from decimal import Decimal
from typing import Optional

from django.db import models

from category.models import Category
from coupon.models import Coupon


class Product(models.Model):
    id: int = models.BigAutoField(primary_key=True, verbose_name="상품 ID")
    name: str = models.CharField(max_length=255, verbose_name="상품명")
    description: str = models.TextField(verbose_name="상품 상세 설명")
    price: int = models.IntegerField(verbose_name="상품 가격")
    category: Category = models.ForeignKey(
        'category.Category', on_delete=models.CASCADE, related_name='products', verbose_name="상품 카테고리")
    discount_rate: float = models.FloatField(default=0.0, verbose_name="할인율")
    coupon_applicable: bool = models.BooleanField(default=False, verbose_name="쿠폰 적용 가능 여부")
    coupon: Optional[Coupon] = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True,
                                                 related_name='products', verbose_name="상품 적용 쿠폰")

    def calculate_discounted_price(self) -> int:
        """할인율을 적용한 가격 계산"""
        discounted_price = Decimal(self.price) * (Decimal('1.00') - Decimal(str(self.discount_rate)))
        return int(discounted_price)

    def calculate_final_price(self) -> int:
        """최종 가격 계산 (쿠폰 적용 포함)"""
        final_price = Decimal(self.calculate_discounted_price())
        if self.coupon_applicable and self.coupon:
            final_price *= (Decimal('1.00') - Decimal(str(self.coupon.discount_rate)))
        return int(final_price)

    def __str__(self) -> str:
        return self.name
