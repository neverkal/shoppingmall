from typing import Optional

from django.db.models import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from common.response import ErrorResponse
from coupon.models import Coupon
from .models import Product
from product.response import ProductDetailResponse
from .serializers import ProductSerializer, ProductDetailSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self) -> "QuerySet[Product]":
        category_id: Optional[str] = self.request.query_params.get('category_id')

        if category_id:
            queryset = Product.objects.filter(category_id=category_id)
        else:
            queryset = Product.objects.all()

        return queryset


class ProductDetailView(APIView):
    """
    상품 상세 정보를 조회하는 API
    - 할인율 적용 가격 및 쿠폰 적용 최종 가격 반환
    """
    @swagger_auto_schema(
        operation_description="상품 상세 정보를 조회합니다.",
        manual_parameters=[
            openapi.Parameter(
                "coupon_code",
                openapi.IN_QUERY,
                description="적용할 쿠폰 코드",
                type=openapi.TYPE_STRING,
            )
        ],
        responses={
            200: ProductDetailSerializer,
            404: openapi.Response(description="상품 또는 쿠폰을 찾을 수 없습니다."),
        },
    )
    def get(self, request, product_id) -> Response:
        # 상품 조회
        try:
            product: Product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return ErrorResponse.not_found("Product not found.")

        # 쿠폰 코드 확인 (쿼리 파라미터)
        coupon_code: Optional[str] = request.query_params.get('coupon_code', None)
        coupon: Optional[Coupon] = None

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
            except Coupon.DoesNotExist:
                return ErrorResponse.not_found("Coupon not found.")

        discounted_price = product.calculate_discounted_price()
        final_price_with_coupon = product.calculate_final_price(coupon=coupon)

        product_detail = ProductDetailResponse(
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

        return Response(product_detail.dict(), status=status.HTTP_200_OK)
