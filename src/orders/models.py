from django.db import models
from foods.models import Food



class Table(models.Model):
    number = models.IntegerField()
    is_reserved = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.number} ({'reserved' if self.is_reserved else 'empty'})"


class Order(models.Model):
    customer = models.IntegerField()
    price = models.FloatField()
    discount = models.FloatField(default=0.0)
    date_submit = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField()
    table=models.ForeignKey(Table,on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.customer


class OrderItem(models.Model):
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    discount = models.FloatField(default=0.0)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.quantity
