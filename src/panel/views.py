from django.shortcuts import render, redirect
from orders.models import Order, Table
from .urls import *

# Create your views here.

def dashboard_staff(request):
    orders = Order.objects.order_by('status')
    tables = Table.objects.all()
    context = {
        'orders': orders ,
        'tables': tables ,
    }
    return render(request,'panel/dashboard_staff.html', context)

def simple_action(view_func):
    def _wrapped_view(request, order_id, *args, **kwargs):
        response = view_func(request, order_id, *args, **kwargs)
        return redirect('dashboard')
    return _wrapped_view

def edit_order(request, order_id):
    pass

@simple_action
def approve_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.approve()