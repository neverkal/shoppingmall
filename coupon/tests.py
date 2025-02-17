from typing import Dict, Any

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from product.models import Product, Category
from .models import Coupon
from .serializers import CouponSerializer


# Create your tests here.
class CouponModelTest(TestCase):
    def setUp(self) -> None:
        self.coupon: Coupon = Coupon.objects.create(code="테스트10", discount_rate=0.1)

    def test_coupon_creation(self) -> None:
        self.assertEqual(self.coupon.code, "테스트10")
        self.assertEqual(self.coupon.discount_rate, 0.1)

    def test_coupon_str_method(self) -> None:
        self.assertEqual(str(self.coupon), "테스트10")


class CouponSerializerTest(TestCase):
    def setUp(self) -> None:
        self.coupon_attributes: Dict[str, Any] = {
            'code': '할인20',
            'discount_rate': 0.2
        }
        self.serializer: CouponSerializer = CouponSerializer(data=self.coupon_attributes)

    def test_contains_expected_fields(self) -> None:
        data: Dict[str, Any] = self.serializer.initial_data
        self.assertCountEqual(data.keys(), ['code', 'discount_rate'])

    def test_field_content(self) -> None:
        data: Dict[str, Any] = self.serializer.initial_data
        self.assertEqual(data['code'], self.coupon_attributes['code'])
        self.assertEqual(data['discount_rate'], self.coupon_attributes['discount_rate'])


class CouponViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.coupon: Coupon = Coupon.objects.create(code="뷰테스트", discount_rate=0.15)

    def test_get_all_coupons(self) -> None:
        url: str = reverse('coupon-list')
        response: Response = self.client.get(url)
        coupons = Coupon.objects.all()
        serializer: CouponSerializer = CouponSerializer(coupons, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_coupon(self) -> None:
        url: str = reverse('coupon-detail', args=[self.coupon.id])
        response: Response = self.client.get(url)
        coupon: Coupon = Coupon.objects.get(id=self.coupon.id)
        serializer: CouponSerializer = CouponSerializer(coupon)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CouponApplyViewTest(APITestCase):
    def setUp(self) -> None:
        self.category: Category = Category.objects.create(name="테스트 카테고리")
        self.product: Product = Product.objects.create(
            name="테스트 상품",
            description="테스트 설명",
            price=100.00,
            category=self.category,
            discount_rate=0.1,
            coupon_applicable=True
        )
        self.coupon: Coupon = Coupon.objects.create(code="적용10", discount_rate=0.1)
        self.url: str = reverse('apply-coupon')

    def test_apply_coupon_success(self) -> None:
        data: Dict[str, Any] = {
            'product_id': self.product.id,
            'coupon_code': self.coupon.code
        }
        response: Response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('final_price_with_coupon', response.data)

    def test_apply_coupon_product_not_found(self) -> None:
        data: Dict[str, Any] = {
            'product_id': 9999,  # 존재하지 않는 상품 ID
            'coupon_code': self.coupon.code
        }
        response: Response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_apply_coupon_coupon_not_found(self) -> None:
        data: Dict[str, Any] = {
            'product_id': self.product.id,
            'coupon_code': 'VALIDCODE123'  # 존재하지 않는 쿠폰 코드
        }
        response: Response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_apply_coupon_not_applicable(self) -> None:
        self.product.coupon_applicable = False
        self.product.save()
        data: Dict[str, Any] = {
            'product_id': self.product.id,
            'coupon_code': self.coupon.code
        }
        response: Response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_apply_coupon_invalid_code_format(self) -> None:
        data: Dict[str, Any] = {
            'product_id': self.product.id,
            'coupon_code': 'invalid_code'  # 소문자와 특수문자를 포함한 잘못된 형식의 쿠폰 코드
        }
        response: Response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('쿠폰 코드는 영대문자 또는 한글, 숫자만 입력 가능합니다.', str(response.data))

    def test_apply_coupon_valid_code_format(self) -> None:
        valid_coupon: Coupon = Coupon.objects.create(code="VALIDCODE123", discount_rate=0.15)
        data: Dict[str, Any] = {
            'product_id': self.product.id,
            'coupon_code': valid_coupon.code
        }
        response: Response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('final_price_with_coupon', response.data)
