from django.shortcuts import render
from orders.models import Order
from django.db.models import Sum , Count
import datetime

# Create your views here.
def dashboard(request):
    all_orders = Order.objects.all()
    last_days = datetime.datetime.today() - datetime.timedelta()
    last_7_days = datetime.datetime.today() - datetime.timedelta(7)
    last_30_days = datetime.datetime.today() - datetime.timedelta(30)
    
    #money made of order
    
    price_for_each_day_of_month = all_orders.filter(created_at__gte=last_30_days).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Sum('price'))
    
    
    price_for_each_day_of_week = all_orders.filter(created_at__gte=last_7_days).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Sum('price'))
    
    #count of orders
    
    count_of_order_for_each_day_of_month = all_orders.filter(created_at__gte=last_30_days).\
    extra({'day' : "date(created_at)"}).\
    values('day').\
    annotate(created_count=Count('id'))
    
    count_of_order_day_of_month = all_orders.filter(created_at__gte=last_7_days).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(created_count=Count('price'))