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
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="상품 ID"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="상품명"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="상품 설명"),
                'price': openapi.Schema(type=openapi.TYPE_INTEGER, description="상품 가격"),
                'category': openapi.Schema(type=openapi.TYPE_STRING, description="상품 카테고리"),
                'discount_rate': openapi.Schema(type=openapi.TYPE_NUMBER, description="할인율"),
                'coupon_applicable': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="쿠폰 적용 가능 여부"),
                'discounted_price': openapi.Schema(type=openapi.TYPE_INTEGER, description="상품 할인 가격"),
                'final_price_with_coupon': openapi.Schema(type=openapi.TYPE_INTEGER, description="상품 최종 가격"),
            },
            required=[
                'id', 'name', 'description', 'price', 'category', 'discount_rate', 'coupon_applicable',
                'discounted_price', 'final_price_with_coupon'
            ]
        )
