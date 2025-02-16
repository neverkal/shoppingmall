from django.urls import path
from .views import ProductDetailView, ProductListView


urlpatterns = [
    path('<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('', ProductListView.as_view(), name='product-list'),
]
