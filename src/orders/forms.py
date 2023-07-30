from django import forms
from django.core.validators import RegexValidator
from users.models import PhoneNumberField


phone_validator = RegexValidator(r"(((\+|00)(98))|0)?9\d{2}-?\d{3}-?\d{4}")
class CustomerLoginForm(forms.Form):
    phone = PhoneNumberField(validators=[phone_validator], unique=True, max_length=20)
    image=forms.ImageField(upload_to='static/',blank=True,null=True)

