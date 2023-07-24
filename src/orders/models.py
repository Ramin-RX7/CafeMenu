from django.db import models
from foods.models import Food

class Order(models.Model):
    items = models.IntegerField()
    price = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # TODO customer model

    def __str__(self) -> str:
        return self.items
    
class OrderItem(models.Model):
    quantity = models.IntegerField()
    price = models.FloatField()
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.quantity
