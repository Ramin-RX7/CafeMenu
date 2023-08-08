from django import forms
from django.core.validators import RegexValidator



phone_validator = RegexValidator(r"(((\+|00)(98))|0)?9\d{2}-?\d{3}-?\d{4}")
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
