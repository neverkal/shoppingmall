from django.db import models


class Coupon(models.Model):
    id: int = models.BigAutoField(primary_key=True)
    code: str = models.CharField(max_length=50, unique=True)
    discount_rate: float = models.FloatField()

    def __str__(self) -> str:
        return self.code
