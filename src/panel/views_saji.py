import datetime
from django.shortcuts import render
from django.db.models import Sum , Count , Q

from foods.models import Category,Food
from orders.models import Order,OrderItem
from datetime import timedelta



def dashboard(request):
    
    all_orders = Order.objects.all()
    today_date = datetime.datetime.today()
    week_day = today_date.weekday()
    to_day = today_date.day

    last_day = today_date - datetime.timedelta(1)
    
    this_week = today_date - datetime.timedelta(week_day)
    last_week = today_date - datetime.timedelta(week_day+7)
    
    this_month = today_date - datetime.timedelta(to_day)
    last_month = today_date - datetime.timedelta(to_day + 30)
      
    last_7_days = datetime.datetime.today() - datetime.timedelta(7)
    last_30_days = datetime.datetime.today() - datetime.timedelta(30)
    
    def dict_to_list(data:dict, value_item:str=None,thisweek=False,lastweek=False,last7days=False,thismonth=False,lastmonth=False,last30days=False):
        list_data = []
        if thisweek:
            for i in range(int((today_date - this_week).days)+1):
                date = str((this_week + datetime.timedelta(i)).date())
                # print("this",date)
                for item in data:
                    if item['day'] == date:
                        list_data.append(item[value_item])
                        break
                else:
                    list_data.append(0)
        
        if lastweek:
            for i in range(int((this_week - last_week).days)):
                date = str((last_week + datetime.timedelta(i)).date())
                # print("last",date)
                for item in data:
                    if item['day'] == date:
                        list_data.append(item[value_item])
                        break
                else:
                    list_data.append(0)
        
        if last7days:
            for i in range(int((today_date - last_7_days).days)):
                date = str((last_7_days+ datetime.timedelta(i)).date())
                for item in data:
                    if item['day'] == date:
                        list_data.append(item[value_item])
                        break
                else:
                    list_data.append(0)
                
        if thismonth:
            for i in range(int((today_date - this_month).days)+1):
                date = str((this_month + datetime.timedelta(i)).date())
                for item in data:
                    if item['day'] == date:
                        list_data.append(item[value_item])
                        break
                else:
                    list_data.append(0)
            
        if lastmonth:
            for i in range(int((this_month - last_month).days)+1):
                date = str((last_month + datetime.timedelta(i)).date())
                for item in data:
                    if item['day'] == date:
                        list_data.append(item[value_item])
                        break
                else:
                    list_data.append(0)
                
        if last30days:
            for i in range(int((today_date - last_30_days).days)+1):
                date = str((last_30_days+ datetime.timedelta(i)).date())
                for item in data:
                    if item['day'] == date:
                        list_data.append(item[value_item])
                        break
                else:
                    list_data.append(0)
        return list_data

    # count of order part
    count_order_hour_today =[]
    for i in range(0,24):
        hour = f'{i}'
        data = all_orders.filter(Q(created_at__date=today_date) & Q(created_at__hour__gte=i) & Q(created_at__hour__lt=i+1))\
        .count()
        if data:
            count_order_hour_today.append(data)
        else:
            count_order_hour_today.append(0)
            
            
    count_order_hour_last_day = []
    for i in range(0,24):
        hour = f'{i}'
        data = all_orders.filter(Q(created_at__date=last_day) & Q(created_at__hour__gte=i) & Q(created_at__hour__lt=i+1))\
        .count()
        if data:
            count_order_hour_last_day.append(data)
        else:
            count_order_hour_last_day.append(0)

     
    count_this_week =list(all_orders.filter(Q(created_at__date__gte = this_week)).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Count('id')))
    count_order_this_week = dict_to_list(data=count_this_week,value_item='count',thisweek=True)

            
    count_last_week = list(all_orders.filter(Q(created_at__date__gte = last_week) & Q(created_at__date__lt = this_week)).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Count('id')))
    count_order_last_week = dict_to_list(data=count_last_week,value_item='count',lastweek=True)

    
    count_this_month =list(all_orders.filter(Q(created_at__date__gte = this_month)).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Count('id')))
    count_order_this_month = dict_to_list(data=count_this_month,value_item='count',thismonth=True)
    
    count_last_month = list(all_orders.filter(Q(created_at__date__gte = last_month) & Q(created_at__date__lt = this_month)).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Count('id')))
    count_order_last_month = dict_to_list(data=count_last_month,value_item='count',lastmonth=True)
    

    count_week =list(all_orders.filter(Q(created_at__date__gte=last_7_days)).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Count('id')))
    count_order_for_7_dasy_past = dict_to_list(data=count_week,value_item='count',last7days=True)
    
    count_month = list(all_orders.filter(Q(created_at__date__gte=last_30_days)).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Count('id')))
    count_order_for_30_day_past = dict_to_list(data=count_month,value_item='count',last30days=True)
   
    context ={
        "sales": {
            "comparative":{
                "day"  : {"old":count_order_hour_last_day,"new":count_order_hour_today},
                "week" : {"old":count_order_last_week,"new":count_order_this_week},
                "month": {"old":count_order_last_month,"new":count_order_this_month},
            },
            "relative":{
                "day"  : count_order_hour_last_day,
                "week" : count_order_for_7_dasy_past,
                "month": count_order_for_30_day_past,
            }
        }
    }
    
    return render(request, "panel/home.html",context)
