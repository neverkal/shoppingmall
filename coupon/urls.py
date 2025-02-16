from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CouponViewSet, CouponApplyView

router = DefaultRouter()
router.register('', CouponViewSet)

urlpatterns = [
    path('apply-coupon/', CouponApplyView.as_view(), name='apply-coupon'),
    path('', include(router.urls)),
]