from django.urls import path
from .views import CouponApplyView, CouponListView, CouponDetailView

urlpatterns = [
    path('apply-coupon/', CouponApplyView.as_view(), name='apply-coupon'),
    path('', CouponListView.as_view(), name='coupon-list'),
    path('<int:pk>/', CouponDetailView.as_view(), name='coupon-detail'),
]
