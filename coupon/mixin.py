from drf_yasg import openapi
from rest_framework.exceptions import NotFound

from coupon.models import Coupon


class CouponMixin:
    @staticmethod
    def get_coupon(coupon_code: str) -> Coupon:
        try:
            return Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            raise NotFound("Coupon not found.")

    @staticmethod
    def get_coupon_by_pk(pk: int) -> Coupon:
        try:
            return Coupon.objects.get(pk=pk)
        except Coupon.DoesNotExist:
            raise NotFound("Coupon not found.")


class CouponApplyResponseMixin:
    @staticmethod
    def get_coupon_apply_response_schema():
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="상품ID"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="상품명"),
                'price': openapi.Schema(type=openapi.TYPE_INTEGER, description="상품 가격"),
                'discount_rate': openapi.Schema(type=openapi.TYPE_NUMBER, description="상품 할인율"),
                'discounted_price': openapi.Schema(type=openapi.TYPE_INTEGER, description="상품 할인가"),
                'final_price_with_coupon': openapi.Schema(type=openapi.TYPE_INTEGER, description="최종 할인가"),
            },
            required=[
                'id', 'name', 'price', 'discount_rate', 'discounted_price', 'final_price_with_coupon'
            ]
        )
