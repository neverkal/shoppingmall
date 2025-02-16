from typing import Optional
from urllib.request import Request

from rest_framework import serializers

from coupon.models import Coupon
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields: list[str] = [
            'id', 'name', 'description', 'price', 'category',
            'discount_rate', 'coupon_applicable'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    final_price_with_coupon = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields: list[str] = [
            'id', 'name', 'description', 'price', 'category',
            'discount_rate', 'coupon_applicable', 'discounted_price', 'final_price_with_coupon'
        ]

    def get_discounted_price(self, obj: Product) -> int:
        return obj.calculate_discounted_price()

    def get_final_price_with_coupon(self, obj: Product) -> int:
        coupon = self._get_coupon_from_request()
        return obj.calculate_final_price(coupon=coupon) if coupon else obj.calculate_discounted_price()

    def _get_coupon_from_request(self) -> Optional[Coupon]:
        request: Optional[Request] = self.context.get('request')
        coupon_code: Optional[str] = request.query_params.get('coupon_code') if request else None

        if not coupon_code:
            return None

        try:
            return Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            return None
