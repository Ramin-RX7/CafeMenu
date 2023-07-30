from django.shortcuts import render,redirect

from .models import Order


def index(request):
    orders  = Order.objects.all()
    context = {"orders": orders }
    return render(request,'orders/order_list.html',context)
def order_list(request):
    return redirect("index")


def order_details(request,id):
    order = Order.objects.get(id=id)
    context = {"order": order}
    return render(request,'orders/order_details.html',context)


def cart(request):
    c_rt = None
    context = {"c_rt": c_rt}
    return render(request,'orders/cart.html',context)
