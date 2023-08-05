from django import forms
from .models import User

class UserLogInForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('phone')