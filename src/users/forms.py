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



class ChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name', 'is_staff', 'is_active','groups','user_permissions','password', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False

    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        elif not self.cleaned_data['password'] and user.pk:
            old_user = User.objects.get(pk=user.pk)
            user.password = old_user.password
        if commit:
            user.save()
        return user
