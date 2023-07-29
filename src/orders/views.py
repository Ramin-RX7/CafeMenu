from django.shortcuts import render
from django.http import HttpResponse
from .models import Order,OrderItem
# Create your views here.

def order_list(request):
    orders  = Order.objects.all()
    context = {"orders": orders }
    return render(request,'orders/order_list.html',context)


def order_details(request,id):
    order = Order.objects.get(id=id)
    context = {"order": order}
    return render(request,'orders/order_details.html',context)


def cart(request):
    c_rt = None
    context = {"c_rt": c_rt}
    return render(request,'orders/cart.html',context)