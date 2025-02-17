from rest_framework.exceptions import NotFound

from product.models import Product


class ProductMixin:
    @staticmethod
    def get_product(product_id: int) -> Product:
        try:
            return (Product.objects
                    .select_related("category")
                    .select_related("coupon").get(id=product_id)
                    )
        except Product.DoesNotExist:
            raise NotFound("Product not found.")
