from django.db import models


class Category(models.Model):
    id: int = models.BigAutoField(primary_key=True, verbose_name="카테고리 ID")
    name: str = models.CharField(max_length=100, verbose_name="카테고리명")

    def __str__(self) -> str:
        return self.name
