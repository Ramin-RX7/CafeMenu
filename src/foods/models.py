from django.db import models
from main.models import BaseModel



class Category(BaseModel):
    title = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/categories/', null=True)

    def __str__(self) -> str:
        return self.title


class Food(BaseModel):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/foods/', null=True)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    discount = models.DecimalField(decimal_places=1, max_digits=3, default=0.0)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
