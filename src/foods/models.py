from django.db import models
from main.models import BaseModel



class Category(BaseModel):
    title = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to = 'images/categories/', default="/images/categories/default.jpeg")

    def __str__(self) -> str:
        return self.title


class Food(BaseModel):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to = 'images/foods/', default="/images/foods/default.jpg")
    price = models.FloatField()
    discount = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.title
