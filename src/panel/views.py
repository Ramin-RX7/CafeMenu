from django.shortcuts import render
from orders.models import Order,OrderItem
from foods.models import Category,Food
from django.db.models import Sum , Count , Q
import datetime

# Create your views here.
def dashboard(request):
    all_orders = Order.objects.all()
    last_days = datetime.datetime.today()
    last_7_days = datetime.datetime.today() - datetime.timedelta(7)
    last_30_days = datetime.datetime.today() - datetime.timedelta(30)
    
    #-----------------------------------------------------------------------------------
    
    # price of sales part
    
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

    #----------------------------------------------------------------------------------------

    # count of order part
    
    count_order_for_each_hour_of_last_day = {} 
    for i in range(7,last_days.hour):
        hour = f'{i}'
        data = all_orders.filter(Q(created_at__date=last_days) & Q(created_at__hour__gte=i) & Q(created_at__hour__lt=i+1))\
        .values('price').annotate(count=Count('id'))
        if data:
            count_order_for_each_hour_of_last_day[hour]=data[0]['count']
        else:
            count_order_for_each_hour_of_last_day[hour]=0
    
    count_order_for_each_day_of_week ={}
    price_week = all_orders.filter(created_at__gte=last_7_days).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Count('id'))
    for k in price_week:
        count_order_for_each_day_of_week[k['day']]=k['count']
        
    count_order_for_each_day_of_month={}              
    price_month = all_orders.filter(created_at__gte=last_30_days).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Count('id'))
    for k in price_month:
        count_order_for_each_day_of_month[k['day']]=k['count']
    
    total_count = all_orders.aaggregate(count=Count('id'))
    
    #----------------------------------------------------------------------------------------
    
    # count of food_items sold part
    
    orderitems = OrderItem.objects.all()
    foods = Food.objects.all()
    foods = [i['customer'] for i in foods.values('customer')]
    info = {}
    for food_name in foods:
        count_of_fooditem_sold_hour_of_last_day = {}
        for i in range(7,last_days.hour):
            hour = f'{i}'
            data = orderitems.filter(Q(food=food_name) & Q(order__status='paid') & Q(created_at__date=last_days) & Q(created_at__hour__gte=i) & Q(created_at__hour__lt=i+1))\
            .values('id').annotate(count=Sum('quantity'))
            if data:
                count_of_fooditem_sold_hour_of_last_day[hour]=data[0]['count']
            else:
                count_of_fooditem_sold_hour_of_last_day[hour]=0
        info[f'{food_name}-hour']=count_of_fooditem_sold_hour_of_last_day
    
        count_of_fooditem_sold_for_each_day_of_week ={}
        price_week = all_orders.filter(Q(food=food_name) & Q(order__status='paid') & Q(created_at__gte=last_7_days)).\
        extra({'day':"date(created_at)"}).\
        values('day').annotate(count=Sum('quantity'))
        for k in price_week:
            count_of_fooditem_sold_for_each_day_of_week[k['day']]=k['count']
        info[f'{food_name}-week']=count_of_fooditem_sold_for_each_day_of_week
        
        
        count_of_fooditem_sold_for_each_day_of_month={}              
        price_month = all_orders.filter(Q(food=food_name) & Q(order__status='paid') & Q(created_at__gte=last_7_days)).\
        extra({'day':"date(created_at)"}).\
        values('day').annotate(count=Sum('quantity'))
        for k in price_month:
            count_of_fooditem_sold_for_each_day_of_month[k['day']]=k['count']
        info[f'{food_name}-month']=count_of_fooditem_sold_for_each_day_of_month
    
        info[f'{food_name}_total_count'] = all_orders.aaggregate(count=Sum('quantity'))
    
    #----------------------------------------------------------------------------------------
    
    # count of category sold part