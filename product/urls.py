from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductDetailView

router = DefaultRouter()
router.register('', ProductViewSet)

urlpatterns = [
    path('<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('', include(router.urls)),
]
