from typing import Any

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from product.mixin import ProductMixin
from product.models import Product
from .mixin import CouponMixin, CouponApplyResponseMixin
from .models import Coupon
from coupon.response import CouponProductResponse
from .serializers import CouponSerializer, CouponApplySerializer, CouponProductResponseSerializer


class CouponListView(APIView):
    @swagger_auto_schema(
        operation_description="쿠폰 목록을 조회합니다.",
        responses={
            200: CouponSerializer(many=True),
            404: openapi.Response(
                description="Not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    def get(self, request):
        coupons = Coupon.objects.all()
        serializer = CouponSerializer(coupons, many=True)
        return Response(serializer.data)


class CouponDetailView(APIView, CouponMixin):
    @swagger_auto_schema(
        operation_description="특정 쿠폰의 상세 정보를 조회합니다.",
        responses={
            200: CouponSerializer(),
            404: openapi.Response(
                description="Not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    def get(self, request, pk):
        coupon = self.get_coupon_by_pk(pk)
        serializer = CouponSerializer(coupon)
        return Response(serializer.data)


class CouponApplyView(APIView, ProductMixin, CouponMixin, CouponApplyResponseMixin):

    @swagger_auto_schema(
        operation_description="상품에 쿠폰을 적용합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="상품ID"),
                'coupon_code': openapi.Schema(type=openapi.TYPE_STRING, description="적용할 쿠폰 코드"),
            },
            required=['product_id', 'coupon_code']
        ),
        responses={
            200: openapi.Response(
                description="Coupon applied successfully",
                schema=CouponApplyResponseMixin.get_coupon_apply_response_schema()
            ),
            404: openapi.Response(
                description="Not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        serializer = CouponApplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = self.get_product(serializer.validated_data['product_id'])
        coupon = self.get_coupon(serializer.validated_data['coupon_code'])

        if not product.coupon_applicable:
            raise ParseError("Coupon cannot be applied to this product.")

        product.coupon = coupon
        product.save()

        response_data = self.create_product_response(product)
        response_serializer = CouponProductResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create_product_response(product: Product) -> dict:
        return {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'discount_rate': product.discount_rate,
            'discounted_price': product.calculate_discounted_price(),
            'final_price_with_coupon': product.calculate_final_price(),
        }

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
