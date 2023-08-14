import datetime
import json

from django.shortcuts import render
from django.db.models import Sum , Count , Q

from foods.models import Category,Food
from orders.models import Order,OrderItem

from main.models import BaseModel
from datetime import timedelta
from django.http import JsonResponse
from django.db.models.functions import ExtractHour

def json_api(request):
    from django.http import HttpResponse
    context = {
        "sales": {
            "comparative":{
                "week" : {"old":[10,15,2,6,4,8,7] , "new":[5,7,6,2,4,5,3]},
            },
            "relative": {
                "day": [6, 1, 13, 2, 12, 15, 13, 6, 11, 15, 9, 7, 8, 9, 1, 1, 1, 4, 7, 6, 9, 3, 14, 3, 7, 13, 1, 15, 6, 13],
                "week": [5,8,6,7,5,2,12]
            }
        },
    }
    return HttpResponse(json.dumps(context))


def analytics(request):
    return render(request, "panel/dashboard_manager.html", {})






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
    count_week = all_orders.filter(created_at__gte=last_7_days).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Count('id'))
    for k in count_week:
        count_order_for_each_day_of_week[k['day']]=k['count']

    count_order_for_each_day_of_month={}
    count_month = all_orders.filter(created_at__gte=last_30_days).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Count('id'))
    for k in count_month:
        count_order_for_each_day_of_month[k['day']]=k['count']

    total_count = all_orders.filter(status="Paid").aaggregate(count=Count('id'))

    #----------------------------------------------------------------------------------------

    # count of food_items sold part

    orderitems = OrderItem.objects.all()
    foods = Food.objects.all()
    foods = [i['title'] for i in foods.values('title')]
    info = {}
    for food_name in foods:
        count_of_fooditem_sold_hour_of_last_day = {}
        for i in range(7,last_days.hour):
            hour = f'{i}'
            data = orderitems.filter(Q(food__title=food_name) & Q(order__status='paid') & Q(Order__created_at__date=last_days) & Q(Order__created_at__hour__gte=i) & Q(Order__created_at__hour__lt=i+1))\
            .values('id').annotate(count=Sum('quantity'))
            if data:
                count_of_fooditem_sold_hour_of_last_day[hour]=data[0]['count']
            else:
                count_of_fooditem_sold_hour_of_last_day[hour]=0
        info[f'{food_name}-day']=count_of_fooditem_sold_hour_of_last_day

        count_of_fooditem_sold_for_each_day_of_week ={}
        count_week_food = orderitems.filter(Q(food__title=food_name) & Q(order__status='paid') & Q(order__created_at__gte=last_7_days)).\
        extra({'day':"date(created_at)"}).\
        values('day').annotate(count=Sum('quantity'))
        for k in count_week_food:
            count_of_fooditem_sold_for_each_day_of_week[k['day']]=k['count']
        info[f'{food_name}-week']=count_of_fooditem_sold_for_each_day_of_week


        count_of_fooditem_sold_for_each_day_of_month={}
        count_month_food = orderitems.filter(Q(food__title=food_name) & Q(order__status='paid') & Q(order__created_at__gte=last_30_days)).\
        extra({'day':"date(created_at)"}).\
        values('day').annotate(count=Sum('quantity'))
        for k in count_month_food:
            count_of_fooditem_sold_for_each_day_of_month[k['day']]=k['count']
        info[f'{food_name}-month']=count_of_fooditem_sold_for_each_day_of_month

        info[f'{food_name}_total_count'] = orderitems.filter(Q(food__title=food_name) & Q(order__status='paid')).aaggregate(count=Sum('quantity'))

    #----------------------------------------------------------------------------------------

    # count of category sold part
    categories = Category.objects.all()
    categories = [i['customer'] for i in foods.values('customer')]
    info_category = {}
    for category in categories:
        count_of_category_sold_hour_of_last_day = {}
        for i in range(7,last_days.hour):
            hour = f'{i}'
            data = orderitems.filter(Q(food__category__title=category) & Q(order__status='paid') & Q(order__created_at__date=last_days) & Q(order__created_at__hour__gte=i) & Q(order__created_at__hour__lt=i+1))\
            .values('id').annotate(count=Sum('quantity'))
            if data:
                count_of_category_sold_hour_of_last_day[hour]=data[0]['count']
            else:
                count_of_category_sold_hour_of_last_day[hour]=0
        info_category[f'{category}-hour']=count_of_category_sold_hour_of_last_day

        count_of_category_sold_for_each_day_of_week ={}
        count_category_week = orderitems.filter(Q(food__category__title=category) & Q(order__status='paid') & Q(order__created_at__gte=last_7_days)).\
        extra({'day':"date(created_at)"}).\
        values('day').annotate(count=Sum('quantity'))
        for k in count_category_week:
            count_of_category_sold_for_each_day_of_week[k['day']]=k['count']
        info_category[f'{category}-week']=count_of_category_sold_for_each_day_of_week


        count_of_category_sold_for_each_day_of_month={}
        count_category_month = orderitems.filter(Q(food__category__title=category) & Q(order__status='paid') & Q(order__created_at__gte=last_7_days)).\
        extra({'day':"date(created_at)"}).\
        values('day').annotate(count=Sum('quantity'))
        for k in count_category_month:
            count_of_category_sold_for_each_day_of_month[k['day']]=k['count']
        info_category[f'{category}-month']=count_of_category_sold_for_each_day_of_month

        info_category[f'{category}_total_count'] = orderitems.filter(Q(food__category__title=category) & Q(order__status='paid')).aaggregate(count=Sum('quantity'))

        context = {
                    "sales": {
                        "day" : price_for_each_hour_of_last_day,
                        "week": price_for_each_day_of_week,
                        "month": price_for_each_day_of_month,
                        "total": total_price
                        },
                    "food_items": {
                        "food":info
                        },
                    "orders": {
                        "day" : count_order_for_each_hour_of_last_day,
                        "week": count_order_for_each_day_of_week,
                        "month": count_order_for_each_day_of_month,
                        "total": total_count
                    },
                    "categories": {
                        'category':info_category
                    }
                    }

        return render(request,'panel/dashboard_manager.html',context)
    
    #----------------------------------------------------------------------------------------

    # Get top 5 peak business hours in month, year
    def get_top_peak_hours(request, year, month):
        start_date = datetime(year, month, 1)
        end_date = start_date.replace(month=month+1) - timedelta(days=1)
        
        top_5_in_year = BaseModel.objects.filter(created_at__year=year).annotate(hour=ExtractHour('created_at')).values('hour').annotate(count=Count('id')).order_by('-count')[:5]
        top_5_in_month = BaseModel.objects.filter(created_at__range=(start_date, end_date)).annotate(hour=ExtractHour('created_at')).values('hour').annotate(count=Count('id')).order_by('-count')[:5]

        data = {"year": list(top_5_in_year), "month": list(top_5_in_month)}
        return JsonResponse(data)
    
    #----------------------------------------------------------------------------------------

    # Get top 5 peak business hours in month, year
    