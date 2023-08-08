from django import forms
from django.core.validators import RegexValidator
from users.models import PhoneNumberField
from orders.models import OrderItem,Order
from django.forms import ModelForm






class EditOrderItemForm(ModelForm):
    id = forms.IntegerField()
    class Meta:
        model = OrderItem
        fields = ['food', 'quantity', 'unit_price', 'discount']


class EditOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"