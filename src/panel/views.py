from django.shortcuts import render
from orders.models import Order
from django.db.models import Sum , Count , Q
import datetime

# Create your views here.
def dashboard(request):
    all_orders = Order.objects.all()
    last_days = datetime.datetime.today()
    last_7_days = datetime.datetime.today() - datetime.timedelta(7)
    last_30_days = datetime.datetime.today() - datetime.timedelta(30)
    
    # price for each hour of day
    price_for_each_hour_of_last_day = {} 
    for i in range(0,last_days.hour):
        hour = f'{i}'
        data = all_orders.filter(Q(status="Paid") & Q(created_at__date=last_days) & Q(created_at__hour__gte=i) & Q(created_at__hour__lt=i+1))\
        .values('price').annotate(total_pirce =Sum('price'))
        if data:
            price_for_each_hour_of_last_day[hour]=data[0]['total_pirce']
        else:
            price_for_each_hour_of_last_day[hour]=0
    
    price_for_each_day_of_week ={}
    price_week = all_orders.filter(Q(status="Paid") & Q(created_at__gte=last_7_days)).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(price=Sum('price'))
    for k in price_week:
        price_for_each_day_of_week[k['day']]=k['price']
        
    price_for_each_day_of_month={}              
    price_month = all_orders.filter(Q(status="Paid") & Q(created_at__gte=last_30_days)).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(price=Sum('price'))
    for k in price_month:
        price_for_each_day_of_month[k['day']]=k['price']
    
    total_price = all_orders.filter(status="Paid").aaggregate(total=Sum('price'))
