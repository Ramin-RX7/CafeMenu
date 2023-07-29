from django.shortcuts import render
from django.http import HttpResponse
from .models import Order,OrderItem
# Create your views here.

def order_list(request):
    orders  = Order.objects.all()
    return render(request,'Order/order_list.html',{"orders": orders })

def order_details(request,pk):
    order = Order.objects.get(id=pk)
    return render(request,'Order/order_details.html',{"order": order})