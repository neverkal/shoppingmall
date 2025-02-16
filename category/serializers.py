from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model: Category = Category
        fields: list[str] = ['id', 'name']
