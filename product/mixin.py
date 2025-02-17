from drf_yasg import openapi
from rest_framework.exceptions import NotFound

from product.models import Product


class ProductMixin:
    @staticmethod
    def get_product(product_id: int) -> Product:
        try:
            return (Product.objects
                    .select_related("category")
                    .select_related("coupon").get(id=product_id)
                    )
        except Product.DoesNotExist:
            raise NotFound("Product not found.")


class ProductResponseMixin:
    @staticmethod
    def get_product_response_schema():
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'price': openapi.Schema(type=openapi.TYPE_INTEGER),
                'category': openapi.Schema(type=openapi.TYPE_STRING),
                'discount_rate': openapi.Schema(type=openapi.TYPE_NUMBER),
                'coupon_applicable': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'discounted_price': openapi.Schema(type=openapi.TYPE_INTEGER),
                'final_price_with_coupon': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=[
                'id', 'name', 'description', 'price', 'category', 'discount_rate', 'coupon_applicable',
                'discounted_price', 'final_price_with_coupon'
            ]
        )
