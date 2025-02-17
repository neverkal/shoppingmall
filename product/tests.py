from typing import Dict, Any

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from category.models import Category
from coupon.models import Coupon
from .models import Product
from .serializers import ProductSerializer


# Create your tests here.
class ProductModelTest(TestCase):
    def setUp(self) -> None:
        self.category: Category = Category.objects.create(name="전자제품")
        self.product: Product = Product.objects.create(
            name="스마트폰",
            description="최신 모델 스마트폰",
            price=1000000,
            category=self.category,
            discount_rate=0.1,
            coupon_applicable=True
        )
        self.coupon: Coupon = Coupon.objects.create(code="할인10", discount_rate=0.1)

    def test_product_creation(self) -> None:
        self.assertEqual(self.product.name, "스마트폰")
        self.assertEqual(self.product.price, 1000000)
        self.assertEqual(self.product.discount_rate, 0.1)
        self.assertTrue(self.product.coupon_applicable)

    def test_calculate_discounted_price(self) -> None:
        self.assertEqual(self.product.calculate_discounted_price(), 900000)

    def test_calculate_final_price_without_coupon(self) -> None:
        self.assertEqual(self.product.calculate_final_price(), 900000)

    def test_calculate_final_price_with_coupon(self) -> None:
        self.product.coupon = self.coupon
        self.product.save()
        self.assertEqual(self.product.calculate_final_price(), 810000)

    def test_calculate_final_price_with_coupon_not_applicable(self) -> None:
        self.product.coupon_applicable = False
        self.product.coupon = self.coupon
        self.product.save()
        self.assertEqual(self.product.calculate_final_price(), 900000)

    def test_calculate_final_price_with_no_coupon_but_applicable(self) -> None:
        self.product.coupon = None
        self.product.save()
        self.assertEqual(self.product.calculate_final_price(), 900000)


class ProductSerializerTest(TestCase):
    def setUp(self) -> None:
        self.category: Category = Category.objects.create(name="전자제품")
        self.product_attributes: Dict[str, Any] = {
            'name': '노트북',
            'description': '고성능 노트북',
            'price': 2000000,
            'category': self.category.id,
            'discount_rate': 0.2,
            'coupon_applicable': True
        }
        self.serializer: ProductSerializer = ProductSerializer(data=self.product_attributes)

    def test_contains_expected_fields(self) -> None:
        data: Dict[str, Any] = self.serializer.initial_data
        self.assertCountEqual(data.keys(), ['name', 'description', 'price', 'category', 'discount_rate', 'coupon_applicable'])

    def test_field_content(self) -> None:
        self.assertTrue(self.serializer.is_valid())
        data: Dict[str, Any] = self.serializer.validated_data
        self.assertEqual(data['name'], self.product_attributes['name'])
        self.assertEqual(data['price'], self.product_attributes['price'])


class ProductViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.category: Category = Category.objects.create(name="전자제품")
        self.product: Product = Product.objects.create(
            name="태블릿",
            description="최신 모델 태블릿",
            price=500000,
            category=self.category,
            discount_rate=0.1,
            coupon_applicable=True
        )

    def test_get_all_products(self) -> None:
        url: str = reverse('product-list')
        response: Response = self.client.get(url)
        products = Product.objects.all()
        serializer: ProductSerializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_filtered_products(self) -> None:
        url: str = reverse('product-list')
        response: Response = self.client.get(url, {'category_id': self.category.id})
        products = Product.objects.filter(category_id=self.category.id)
        serializer: ProductSerializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductDetailViewTest(APITestCase):
    def setUp(self) -> None:
        self.category: Category = Category.objects.create(name="전자제품")
        self.product: Product = Product.objects.create(
            name="스마트워치",
            description="최신 모델 스마트워치",
            price=300000,
            category=self.category,
            discount_rate=0.1,
            coupon_applicable=True
        )
        self.coupon: Coupon = Coupon.objects.create(code="할인10", discount_rate=0.1)
        self.url: str = reverse('product-detail', kwargs={'id': self.product.id})

    def test_get_product_detail_without_coupon(self) -> None:
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['discounted_price'], 270000)
        self.assertEqual(response.data['final_price_with_coupon'], 270000)

    def test_get_product_detail_with_invalid_coupon(self) -> None:
        response: Response = self.client.get(f"{self.url}?coupon_code=잘못된쿠폰")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_nonexistent_product(self) -> None:
        url: str = reverse('product-detail', kwargs={'id': 9999})  # 존재하지 않는 상품 ID
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_product_detail_fields(self) -> None:
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_fields: list[str] = ['id', 'name', 'description', 'price', 'category',
                                      'discount_rate', 'coupon_applicable', 'discounted_price',
                                      'final_price_with_coupon']
        self.assertCountEqual(response.data.keys(), expected_fields)

    def test_product_detail_values(self) -> None:
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.product.id)
        self.assertEqual(response.data['name'], self.product.name)
        self.assertEqual(response.data['description'], self.product.description)
        self.assertEqual(response.data['price'], self.product.price)
        self.assertEqual(response.data['category'], self.category.name)
        self.assertEqual(response.data['discount_rate'], self.product.discount_rate)
        self.assertEqual(response.data['coupon_applicable'], self.product.coupon_applicable)
