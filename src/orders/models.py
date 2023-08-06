from django.db import models
from django.core.validators import RegexValidator
from main.models import BaseModel
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


customer_validator = RegexValidator(r"(((\+|00)(98))|0)?9(?P<operator>\d{2})-?(?P<middle3>\d{3})-?(?P<last4>\d{4})")
class Order(BaseModel):
    customer = models.CharField(max_length=15, validators=[customer_validator])
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    price = models.FloatField(null=True)
    discount = models.FloatField(default=0.0)
    status_field = models.TextChoices("Status","Pending Rejected Approved Delivered Paid")
    status = models.CharField(choices=status_field.choices, max_length=10,default="Pending")

    def __str__(self) -> str:
        return f"{self.customer}"


    def approve(self):
        self.status = "Approved"
        self.save()

    def pay(self):
        self.status = "Paid"
        self.save()

    def save(self, check_price=True):
        if (check_price)  and  (self.price is None):
            raise SystemError("No price given")
        # self.price = sum([item.price for item in self.orderitem_set.all()])
        super().save()


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    discount = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return f"{self.quantity}"
    
    def total_price(self):
        if not self.order.price:
            self.order.price = 0.0
            self.order.price += (self.unit_price * self.quantity)
            self.order.save()
        else:
            raise SystemError