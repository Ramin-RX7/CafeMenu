from django.db import models



class Category(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title


class Food(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    available_quantity = models.IntegerField()
    price = models.FloatField()
    discount = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.title
