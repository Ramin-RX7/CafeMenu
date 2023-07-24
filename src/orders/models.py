from django.db import models
from foods.models import Food

class Order(models.Model):
    items = models.IntegerFields()
    price = models.TextFields()
    discount = models.FloatFields(blank=True, null=True)
    date = models.DateTimeFields(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=CASCADE)

    def __str__(self) -> str:
        return self.items