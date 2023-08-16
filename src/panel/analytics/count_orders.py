import datetime
from django.db.models import Count,Q
from orders.models import Order

from .lib import dict_to_list



def count_orders():

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


    #------------------------------------------------------------------
    sales = {
            "comparative":{
                "day"  : {"old":[],"new":[]},
                "week" : {"old":[],"new":[]},
                "month": {"old":[],"new":[]},
            },
            "relative":{
                "day"  : [],
                "week" : [],
                "month": [],
            }
        }

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
    sales['comparative']["day"]["new"]=count_order_hour_today

    count_order_hour_last_day = []
    for i in range(0,24):
        hour = f'{i}'
        data = all_orders.filter(Q(created_at__date=last_day) & Q(created_at__hour__gte=i) & Q(created_at__hour__lt=i+1))\
        .count()
        if data:
            count_order_hour_last_day.append(data)
        else:
            count_order_hour_last_day.append(0)
    sales['comparative']["day"]["old"] = count_order_hour_today
    sales["relative"]["day"] = count_order_hour_today

    count_this_week =list(all_orders.filter(Q(created_at__date__gte = this_week)).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Count('id')))
    count_order_this_week = dict_to_list(data=count_this_week,value_item='count',thisweek=True)
    sales['comparative']["week"]["new"]=count_order_this_week

    count_last_week = list(all_orders.filter(Q(created_at__date__gte = last_week) & Q(created_at__date__lt = this_week)).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Count('id')))
    count_order_last_week = dict_to_list(data=count_last_week,value_item='count',lastweek=True)
    sales['comparative']["week"]["old"]=count_order_last_week

    count_this_month =list(all_orders.filter(Q(created_at__date__gte = this_month)).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Count('id')))
    count_order_this_month = dict_to_list(data=count_this_month,value_item='count',thismonth=True)
    sales['comparative']["month"]["new"] = count_order_this_month


    count_last_month = list(all_orders.filter(Q(created_at__date__gte = last_month) & Q(created_at__date__lt = this_month)).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Count('id')))
    count_order_last_month = dict_to_list(data=count_last_month,value_item='count',lastmonth=True)
    sales['comparative']["month"]["old"] = count_order_last_month

    count_week =list(all_orders.filter(Q(created_at__date__gte=last_7_days)).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Count('id')))
    count_order_for_7_dasy_past = dict_to_list(data=count_week,value_item='count',last7days=True)
    sales["relative"]["week"]=count_order_for_7_dasy_past


    count_month = list(all_orders.filter(Q(created_at__date__gte=last_30_days)).\
    extra({'day':"date(created_at)"}).\
    values('day').annotate(count=Count('id')))
    count_order_for_30_day_past = dict_to_list(data=count_month,value_item='count',last30days=True)
    sales["relative"]["month"]=count_order_for_30_day_past



    context ={
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

    return context

