from rest_framework.exceptions import NotFound

from category.models import Category


class CategoryMixin:

    @staticmethod
    def get_category(pk: int) -> Category:
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound("Category not found.")
