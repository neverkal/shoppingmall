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
