from typing import Optional, cast

from django.db.models import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from shoppingmall.common.mixin import SwaggerResponseMixin
from .mixin import ProductMixin
from .models import Product
from .serializers import ProductSerializer, ProductDetailSerializer


class ProductListView(APIView):

    @swagger_auto_schema(
        operation_description="상품 목록",
        responses={
            200: ProductSerializer(many=True),
        },
    )
    def get(self, request) -> Response:
        category_id: Optional[str] = request.query_params.get('category_id')
        queryset: QuerySet[Product] = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView, SwaggerResponseMixin, ProductMixin):
    """
    상품 상세 정보를 조회하는 API
    - 할인율 적용 가격 및 쿠폰 적용 최종 가격 반환
    """
    @swagger_auto_schema(
        operation_description="상품 상세 정보",
        responses={
            200: openapi.Response(
                description="쿠폰 상세 정보 조회 성공",
                schema=SwaggerResponseMixin.get_product_response_schema()
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
        },
    )
    def get(self, request, id) -> Response:
        product = self.get_product(id)
        serializer = ProductDetailSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
