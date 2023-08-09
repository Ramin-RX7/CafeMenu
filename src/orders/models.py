from django.db import models

from main.models import BaseModel
from main.validators import phone_validator
from foods.models import Food



class Table(BaseModel):
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



class Order(BaseModel):
    customer = models.CharField(max_length=15, validators=[phone_validator])
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    discount = models.DecimalField(decimal_places=1, max_digits=3, default=0.0)
    status_field = models.TextChoices("Status","Pending Rejected Approved Delivered Paid")
    status = models.CharField(choices=status_field.choices, max_length=10,default="Pending")

    @property
    def price(self):
        return sum([item.unit_price*item.quantity for item in self.orderitem_set.all()])

    @property
    def final_price(self):
        return self.price / 100 * (self.discount or 100)

    def __str__(self) -> str:
        return f"{self.customer}"


    def approve(self):
        self.status = "Approved"
        self.save()
    def reject(self):
        self.status = "Rejected"
        self.save()
    def deliver(self):
        self.status = "Delivered"
        self.save()
    def pay(self):
        self.status = "Paid"
        self.save()

    def save(self, check_items=True):
        if check_items:
            if not self.price:
                raise SystemError("No price given")
        super().save()


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=5)
    discount = models.DecimalField(decimal_places=1, max_digits=3, default=0.0)

    def __str__(self) -> str:
        return f"{self.quantity}"
