from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from common.response.response import ErrorResponse
from product.models import Product
from .models import Coupon
from .response.coupon_product import CouponProduct
from .serializers import CouponSerializer

class CouponViewSet(ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    http_method_names = ["get"]


class CouponApplyView(APIView):

    def post(self, request, *args, **kwargs) -> Response:
        product_id: int = request.data.get('product_id')  # 상품 ID
        coupon_code: str = request.data.get('coupon_code')  # 쿠폰 코드

        # 상품 확인
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return ErrorResponse.not_found("Product not found.")

        # 쿠폰 확인
        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            return ErrorResponse.not_found("Coupon not found.")

        # 쿠폰 적용 가능 여부 확인
        if not product.coupon_applicable:
            return ErrorResponse.bad_request("Coupon cannot be applied to this product.")

        discounted_price = product.calculate_discounted_price()
        final_price_with_coupon = product.calculate_final_price(coupon=coupon)

        dto = CouponProduct(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category.name,
            discount_rate=product.discount_rate,
            coupon_applicable=product.coupon_applicable,
            discounted_price=discounted_price,
            final_price_with_coupon=final_price_with_coupon,
        )

        return Response(dto.dict(), status=status.HTTP_200_OK)