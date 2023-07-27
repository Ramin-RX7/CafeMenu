from django.db import models
from foods.models import Food



class Table(models.Model):
    number = models.IntegerField()
    is_reserved = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.number} ({'reserved' if self.is_reserved else 'empty'})"


class Order(models.Model):
    customer = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.SET_NULL)
    price = models.FloatField()
    discount = models.FloatField(default=0.0)
    date_submit = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField()

    def __str__(self) -> str:
        return self.customer


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    discount = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return self.quantity
