from typing import Any

from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from product.models import Product
from .models import Coupon
from coupon.response import CouponProductResponse
from .serializers import CouponSerializer


class CouponViewSet(ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    http_method_names = ["get"]


class CouponApplyView(APIView):

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        product_id: int = request.data.get('product_id')
        coupon_code: str = request.data.get('coupon_code')

        try:
            product = self._get_product(product_id)
            coupon = self._get_coupon(coupon_code)
        except Product.DoesNotExist:
            raise NotFound("Product not found.")
        except Coupon.DoesNotExist:
            raise NotFound("Coupon not found.")

        if not product.coupon_applicable:
            raise ParseError("Coupon cannot be applied to this product.")

        discounted_price = product.calculate_discounted_price()
        final_price_with_coupon = product.calculate_final_price(coupon=coupon)

        response = self._create_coupon_product_response(product, discounted_price, final_price_with_coupon)

        return Response(response.dict(), status=status.HTTP_200_OK)

    @staticmethod
    def _get_product(product_id: int) -> Product:
        return Product.objects.get(id=product_id)

    @staticmethod
    def _get_coupon(coupon_code: str) -> Coupon:
        return Coupon.objects.get(code=coupon_code)

    @staticmethod
    def _create_coupon_product_response(product: Product, discounted_price: int,
                                        final_price_with_coupon: int) -> CouponProductResponse:
        return CouponProductResponse(
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
