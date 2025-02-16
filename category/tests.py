from typing import Dict

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Category
from .serializers import CategorySerializer


# Create your tests here.
class CategoryModelTest(TestCase):
    def setUp(self) -> None:
        Category.objects.create(name="전자제품")
        Category.objects.create(name="도서")

    def test_category_creation(self) -> None:
        electronics = Category.objects.get(name="전자제품")
        books = Category.objects.get(name="도서")
        self.assertEqual(electronics.name, "전자제품")
        self.assertEqual(books.name, "도서")

    def test_category_str_method(self) -> None:
        electronics = Category.objects.get(name="전자제품")
        self.assertEqual(str(electronics), "전자제품")


class CategorySerializerTest(TestCase):
    def setUp(self) -> None:
        self.category_attributes: Dict[str, str] = {'name': '의류'}
        self.serializer = CategorySerializer(data=self.category_attributes)

    def test_contains_expected_fields(self) -> None:
        data = self.serializer.initial_data
        self.assertCountEqual(data.keys(), ['name'])

    def test_name_field_content(self) -> None:
        data = self.serializer.initial_data
        self.assertEqual(data['name'], self.category_attributes['name'])


class CategoryViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.category1 = Category.objects.create(name="음식")
        self.category2 = Category.objects.create(name="음료")

    def test_get_all_categories(self) -> None:
        url: str = reverse('category-list')
        response = self.client.get(url)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_category(self) -> None:
        url: str = reverse('category-detail', args=[self.category1.id])
        response = self.client.get(url)
        category = Category.objects.get(id=self.category1.id)
        serializer = CategorySerializer(category)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category_not_allowed(self) -> None:
        url: str = reverse('category-list')
        data: Dict[str, str] = {'name': '새 카테고리'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_category_not_allowed(self) -> None:
        url: str = reverse('category-detail', args=[self.category1.id])
        data: Dict[str, str] = {'name': '수정된 카테고리'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_category_not_allowed(self) -> None:
        url: str = reverse('category-detail', args=[self.category1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
