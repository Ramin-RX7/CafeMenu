from django import forms
from django.forms import ModelForm
import datetime
from orders.models import OrderItem,Order
from core.validators import phone_validator

today =datetime.date.today()
last_30days_past = (datetime.datetime.now()-datetime.timedelta(30)).date()



class UserLogInForm(forms.Form):
    phone = forms.CharField()
    otp_code = forms.IntegerField()



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


class SearchbyDate(forms.Form):
    start_date = forms.DateField(required=True, widget = forms.SelectDateWidget(attrs=({'style': 'width: 33%; display: inline-block;'})),initial=datetime.date.today())
    end_date = forms.DateField(required=True  , widget = forms.SelectDateWidget(attrs=({'style': 'width: 33%; display: inline-block;'})),initial=datetime.date.today())

    def clean(self):
        super(SearchbyDate, self).clean()
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        # if start_date < last_30days_past:
            # raise forms.ValidationError("Date cannot be more than 30 days past.")
        if start_date > today:
            raise forms.ValidationError("Start day should be in the past.")
        # if end_date > today:
            # raise forms.ValidationError("End day cant be bigger than today.")
        if end_date < start_date:
            raise forms.ValidationError("End day dhould be bigger than stat day.")
        # if end_date < last_30days_past:
            # raise forms.ValidationError("End day should be bigger than last 30 days past nad start day.")

        return self.cleaned_data
