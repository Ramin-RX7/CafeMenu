from django import forms
from . import models


class CategoryForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.widgets.ClearableFileInput(
            attrs={'accept': 'image/*'}
        ),
        required=False
    )
    delete_image = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'delete-image-checkbox'}))

    class Meta:
        model = models.Category
        fields = '__all__'


class FoodForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.widgets.ClearableFileInput(
            attrs={'accept': 'image/*'}
        ),
        required=False
    )
    delete_image = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'delete-image-checkbox'}))

    class Meta:
        model = models.Food
        fields = '__all__'
