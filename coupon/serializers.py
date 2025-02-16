from rest_framework import serializers
from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model: Coupon = Coupon
        fields: list[str] = ['id', 'code', 'discount_rate']
