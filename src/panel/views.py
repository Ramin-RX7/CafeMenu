from django.shortcuts import render
from orders.models import Order, Table

# Create your views here.

def dashboard_staff(request):
    orders = Order.objects.order_by('status')
    tables = Table.objects.all()
    context = {
        'orders': orders ,
        'tables': tables ,
    }
    return render(request,'panel/dashboard_staff.html', context)