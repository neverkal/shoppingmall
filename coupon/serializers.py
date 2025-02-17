import re

from rest_framework import serializers
from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model: Coupon = Coupon
        fields: list[str] = ['id', 'code', 'discount_rate']


def validate_coupon_code(value):
    if not re.match(r'^[가-힣A-Z0-9]+$', value):
        raise serializers.ValidationError("쿠폰 코드는 영대문자 또는 한글, 숫자만 입력 가능합니다.")
    return value


class CouponApplySerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    coupon_code = serializers.CharField(validators=[validate_coupon_code])


class CouponProductResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.IntegerField()
    discount_rate = serializers.FloatField()
    discounted_price = serializers.IntegerField()
    final_price_with_coupon = serializers.IntegerField()
