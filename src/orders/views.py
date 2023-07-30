from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CustomerLoginForm
# Create your views here.

def order_list(request):
    return HttpResponse("hello world")

def order_details(request):
    return HttpResponse("hello world")

def customer_login(request):
    if request.method == "POST":
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            phone=form.cleaned_data['phone']
            request.session['phone']=phone
    return redirect('menu.html')