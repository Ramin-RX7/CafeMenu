from django.db import models

from core.models import BaseModel
from foods.models import Food
from users.models import User


class Table(BaseModel):
    name = models.CharField(unique=True, max_length=25)
    is_reserved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name} ({'reserved' if self.is_reserved else 'empty'})"

    @classmethod
    def get_available_table(cls):
        tables = cls.objects.all()
        for table in tables:
            if table.is_reserved is False:
                return table



class Order(BaseModel):
    customer = models.ForeignKey(User, models.PROTECT)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    discount = models.DecimalField(decimal_places=1, max_digits=3, default=0.0)
    status_field = models.TextChoices("Status","Pending Rejected Approved Delivered Paid")
    status = models.CharField(choices=status_field.choices, max_length=10,default="Pending")
    responsible_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="assigned_orders")

    @property
    def price(self):
        return sum([item.final_price for item in self.orderitem_set.all()])

    @property
    def final_price(self):
        return round(self.price / 100 * (self.discount or 100), 2)

    def __str__(self) -> str:
        return f"{self.customer}"

    @property
    def get_url_id(self):
        return self.created_at.strftime("%Y%m%d%H%M%S")


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

    def take_responsibility(self, staff:User):
        self.responsible_staff = staff
        self.save()

    def save(self, check_items=True):
        if check_items:
            if not self.price:
                raise SystemError("No price given")
        super().save()


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=5)
    discount = models.DecimalField(decimal_places=1, max_digits=3, default=0.0)

    @property
    def final_price(self):
        return round(((100-self.discount)/100*self.unit_price)*self.quantity, 2)

    def __str__(self) -> str:
        return f"{self.quantity}"

    def save(self, *args, **kwargs):
        related_order_items = OrderItem.objects.filter(order=self.order, food=self.food).exclude(id=self.id)
        if len(related_order_items):
            total_quantity = sum([item.quantity for item in related_order_items])
            for item in related_order_items:
                item.delete()
            self.quantity = total_quantity + self.quantity
        super().save(*args, **kwargs)
