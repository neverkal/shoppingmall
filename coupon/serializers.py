from rest_framework import serializers
from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model: Coupon = Coupon
        fields: list[str] = ['id', 'code', 'discount_rate']


class CouponApplySerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    coupon_code = serializers.CharField()


class CouponProductResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    category = serializers.CharField()
    discount_rate = serializers.FloatField()
    coupon_applicable = serializers.BooleanField()
    discounted_price = serializers.IntegerField()
    final_price_with_coupon = serializers.IntegerField()
