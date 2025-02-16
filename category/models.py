from django.db import models


class Category(models.Model):
    id: int = models.BigAutoField(primary_key=True)
    name: str = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
