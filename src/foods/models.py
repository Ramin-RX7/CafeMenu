from django.db import models

class Category(models.Model):
    title = models.CharFields(max_length=30)
    description = models.TextFields(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

class Food(models.Model):
    title = models.CharFields(max_length=50)
    description = models.TextFields(blank=True, null=True)
    price = models.FloatFields()
    quantity = models.IntegerField()
    discount = models.FloatFields(blank=True, null=True)
    # I set null=True because st we dont have descount
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    # I use protect because we can't delete this table easy and its importent table for our site

    def __str__(self) -> str:
        return self.title