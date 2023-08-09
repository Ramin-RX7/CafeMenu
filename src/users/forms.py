from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

from .models import User



class UserAddForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name', 'is_staff', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name', 'is_staff', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False

    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            self.instance.set_password(password)
        return password
