import datetime
from django.db.models import Sum,Q
from django.db.models.functions import TruncDate ,ExtractHour
from foods.models import Food
from orders.models import OrderItem

from .lib import dict_to_list




def food_items():
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


    food_items = {
            "comparative":{
                "day"  : {"old":{},"new":{}},
                "week" : {"old":{},"new":{}},
                "month": {"old":{},"new":{}},
            },
            "relative":{
                "day"  : {"new":{},"old":None},
                "week" : {"new":{},"old":None},
                "month": {"new":{},"old":None},
            }
        }
    orderitems = OrderItem.objects.all()
    foods = Food.objects.all()
    foods = [i['title'] for i in foods.values('title')]
    
    for food_name in foods:
    
        today_hours = list(orderitems.filter(Q(food__title=food_name) & Q(created_at__date=today_date))\
        .annotate(hour=ExtractHour('order__created_at')).values('hour').annotate(count=Sum('quantity')))
        food_items['comparative']["day"]["new"][food_name] = dict_to_list(today_hours,value_item='count',hour=True)

        last_day_hours = list(orderitems.filter(Q(food__title=food_name) & Q(order__created_at__date=last_day))\
        .annotate(hour=ExtractHour('order__created_at')).values('id').annotate(count=Sum('quantity')))

        food_items['comparative']["day"]["old"][food_name] = dict_to_list(last_day_hours,value_item='count',hour=True)

        food_items["relative"]["day"]["new"][food_name] = dict_to_list(last_day_hours,value_item='count',hour=True)

        count_this_week_food = list(orderitems.filter(Q(food__title = food_name) & Q(order__created_at__date__gte=this_week)).\
        annotate(day=TruncDate('order__created_at')).\
        values('day').annotate(count=Sum('quantity')))
        count_of_fooditem_sold_this_week = dict_to_list(count_this_week_food,value_item='count',thisweek=True)
        food_items['comparative']["week"]["new"][food_name] = sum(count_of_fooditem_sold_this_week)


        count_last_week_food =list(orderitems.filter(Q(food__title=food_name) & Q(order__created_at__date__gte=last_week)& Q(order__created_at__date__lt=this_week)).\
        annotate(day=TruncDate('order__created_at')).\
        values('day').annotate(count=Sum('quantity')))
        count_of_fooditem_sold__last_week = dict_to_list(count_last_week_food,value_item='count',lastweek=True)
        food_items['comparative']["week"]["old"][food_name] = sum(count_of_fooditem_sold__last_week)


        count_week_food = list(orderitems.filter(Q(food__title=food_name) & Q(order__status='paid') & Q(order__created_at__date__gte=last_7_days)).\
        annotate(day=TruncDate('order__created_at')).\
        values('day').annotate(count=Sum('quantity')))
        count_of_fooditem_sold_for_each_day_of_week = dict_to_list(count_week_food,value_item='count',last7days=True)
        food_items["relative"]["week"]["new"][food_name] = sum(count_of_fooditem_sold_for_each_day_of_week)



        count_this_month_food = list(orderitems.filter(Q(food__title=food_name) & Q(order__created_at__date__gte=this_month)).\
        annotate(day=TruncDate('order__created_at')).\
        values('day').annotate(count=Sum('quantity')))
        count_of_fooditem_sold_this_month = dict_to_list(count_this_month_food,value_item='count',thismonth=True)
        food_items['comparative']["month"]["new"][food_name] = sum(count_of_fooditem_sold_this_month)


        count_last_month_food = list(orderitems.filter(Q(food__title=food_name)& Q(order__created_at__date__gte=last_month)& Q(order__created_at__date__lt=this_month)).\
        annotate(day=TruncDate('order__created_at')).\
        values('day').annotate(count=Sum('quantity')))
        count_of_fooditem_sold_last_month = dict_to_list(count_last_month_food,value_item='count',lastmonth=True)
        food_items['comparative']["month"]["old"][food_name] = sum(count_of_fooditem_sold_last_month)


        count_month_food = list(orderitems.filter(Q(food__title=food_name) & Q(order__created_at__date__gte=last_30_days)).\
        annotate(day=TruncDate('order__created_at')).\
        values('day').annotate(count=Sum('quantity')))
        count_of_fooditem_sold_for_each_day_of_month = dict_to_list(count_month_food,value_item='count',last30days=True)
        food_items["relative"]["month"]["new"][food_name] = sum(count_of_fooditem_sold_for_each_day_of_month)

    # print(food_items["comparative"]["day"])
    return food_items
