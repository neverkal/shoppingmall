from tkinter.scrolledtext import example

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixin import CategoryMixin
from .models import Category
from .serializers import CategorySerializer


class CategoryListView(APIView):
    @swagger_auto_schema(
        operation_description="모든 카테고리를 조회합니다.",
        responses={200: CategorySerializer(many=True)}
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetailView(APIView, CategoryMixin):
    @swagger_auto_schema(
        operation_description="특정 카테고리의 상세 정보를 조회합니다.",
        responses={
            200: CategorySerializer(),
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
                        'detail': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            )
        }
    )
    def get(self, request, pk):
        category = self.get_category(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
