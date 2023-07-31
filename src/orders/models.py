from django.db import models
from foods.models import Food



class Table(models.Model):
    name = models.CharField(unique=True, max_length=25)
    is_reserved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name} ({'reserved' if self.is_reserved else 'empty'})"

    @classmethod
    def get_available_table(cls):
        tables = cls.objects.all()
        for table in tables:
            if table.is_reserved == False:
                return table


class Order(models.Model):
    customer = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()
    discount = models.FloatField(default=0.0)
    date_submit = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.customer}"
    
    def approve(self):
        self.is_approved =True
        for item in self.orderitem_set.all():
            if item.food.available_quantity >= item.quantity :
                item.food.available_quantity -= item.quantity
                super().save()
            else:
                raise SystemError

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    discount = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return f"{self.quantity}"
