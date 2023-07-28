from django.shortcuts import render
from django.http import HttpResponse
from .models import Order,OrderItem
# Create your views here.

def order_list(request):
    all_orders = Order.objects.all()
    return render(request,'Order/order_list.html',{"all_orders":all_orders})

def order_details(request,pk):
    order = OrderItem.objects.get(id=pk)
    return render(request,'Order/order_details.html',{"order": order})