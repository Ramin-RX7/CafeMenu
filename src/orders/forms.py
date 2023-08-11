from django import forms

from main.validators import phone_validator



class PhoneInput(forms.widgets.TextInput):
    def __init__(self, *args, **kwargs):
        attrs = kwargs.setdefault('attrs', {})
        attrs['class'] = 'form-control'
        super().__init__(*args, **kwargs)

class CustomerLoginForm(forms.Form):
    phone = forms.CharField(validators=[phone_validator], max_length=20, widget=PhoneInput)
