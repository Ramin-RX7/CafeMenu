from django import forms
from django.forms import ModelForm
from django.core.validators import RegexValidator

from users.models import PhoneNumberField
from orders.models import OrderItem,Order
from foods.models import Food





class EditOrderItemForm(ModelForm):
    id = forms.IntegerField(widget=forms.TextInput(attrs={"readonly":True,"class":"form-control my-1"}),required=False)
    quantity = forms.IntegerField(min_value=1,max_value=100,widget=forms.TextInput(attrs={"class":"form-control my-1"}))
    class Meta:
        model = OrderItem
        fields = ['food', 'quantity']


class EditOrderForm(ModelForm):
    discount = forms.DecimalField(min_value=0.0, max_value=100.0,max_digits=4,widget=forms.TextInput(attrs={"class":"form-control my-1"}))
    customer = forms.CharField(validators=[RegexValidator(r"(((\+|00)(98))|0)?9\d{2}-?\d{3}-?\d{4}")],widget=forms.TextInput(attrs={"class":"form-control my-2"}))
    class Meta:
        model = Order
        fields = ["customer", "discount", "status"]
