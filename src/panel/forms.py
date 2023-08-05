from django import forms
from django.core.validators import RegexValidator



phone_validator = RegexValidator(r"(((\+|00)(98))|0)?9\d{2}-?\d{3}-?\d{4}")
class UserLogInForm(forms.Form):
    phone=forms.IntegerField(validators=[phone_validator])

class UserVerifyForm(forms.Form):
    opt=forms.CharField(min_length=4 ,max_length = 4)