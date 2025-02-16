from typing import Optional

from django.db.models import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer, ProductDetailSerializer


class ProductListView(APIView):

    @swagger_auto_schema(
        operation_description="상품 정보를 조회합니다.",
        responses={
            200: ProductSerializer(many=True),
            404: openapi.Response(description="상품 또는 쿠폰을 찾을 수 없습니다."),
        },
    )
    def get(self, request) -> Response:
        category_id: Optional[str] = request.query_params.get('category_id')

        if category_id:
            queryset: QuerySet[Product] = Product.objects.filter(category_id=category_id)
        else:
            queryset: QuerySet[Product] = Product.objects.all()

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    def get(self, request, id) -> Response:
        # 상품 조회
        try:
            product: Product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found.")

        # ProductDetailSerializer 사용
        serializer = ProductDetailSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
