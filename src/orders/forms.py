from django import forms
from django.core.validators import RegexValidator
from users.models import PhoneNumberField


phone_validator = RegexValidator(r"(((\+|00)(98))|0)?9\d{2}-?\d{3}-?\d{4}")


class PhoneInput(forms.widgets.TextInput):
    def __init__(self, *args, **kwargs):
        attrs = kwargs.setdefault('attrs', {})
        attrs['class'] = 'form-control'
        super().__init__(*args, **kwargs)

class CustomerLoginForm(forms.Form):
    phone = forms.CharField(validators=[phone_validator], max_length=20, widget=PhoneInput)
