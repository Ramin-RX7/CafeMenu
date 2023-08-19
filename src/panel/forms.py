from django import forms
from django.forms import ModelForm

from orders.models import OrderItem,Order
from core.validators import phone_validator



class UserLogInForm(forms.Form):
    phone=forms.CharField(
        validators = [phone_validator],
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Phone"
        }))


class UserVerifyForm(forms.Form):
    otp=forms.CharField(
        min_length=4, max_length=4,
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Code"
        }))



class EditOrderItemForm(ModelForm):
    id = forms.IntegerField(widget=forms.TextInput(attrs={"readonly":True,"class":"form-control my-1"}),required=False)
    quantity = forms.IntegerField(min_value=1,max_value=100,widget=forms.TextInput(attrs={"class":"form-control my-1"}))
    class Meta:
        model = OrderItem
        fields = ['food', 'quantity']

class AddOrderItemForm(ModelForm):
    quantity = forms.IntegerField(min_value=1,max_value=100,widget=forms.TextInput(attrs={"class":"form-control my-1"}))

    def __init__(self, exclude:list[int]=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if exclude is not None:
            self.fields['food'].queryset = self.fields['food'].queryset.exclude(id__in=exclude)

    class Meta:
        model = OrderItem
        fields = ['food', 'quantity']



class EditOrderForm(ModelForm):
    discount = forms.DecimalField(min_value=0.0, max_value=100.0,max_digits=4,widget=forms.TextInput(attrs={"class":"form-control my-1"}))
    customer = forms.CharField(validators=[phone_validator],widget=forms.TextInput(attrs={"class":"form-control my-2"}))
    class Meta:
        model = Order
        fields = ["customer", "discount", "status","table"]
