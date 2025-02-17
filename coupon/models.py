from django.db import models


class Coupon(models.Model):
    id: int = models.BigAutoField(primary_key=True, verbose_name="쿠폰 ID")
    code: str = models.CharField(max_length=50, unique=True, verbose_name="쿠폰 코드")
    discount_rate: float = models.FloatField(verbose_name="쿠폰 할인율")

    def __str__(self) -> str:
        return self.code
