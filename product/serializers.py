from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields: list[str] = [
            'id', 'name', 'description', 'price', 'category',
            'discount_rate', 'coupon_applicable'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
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
        return obj.calculate_final_price()
