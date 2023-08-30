from collections import defaultdict
import datetime
from django.db.models import Sum,Q
from django.db.models.functions import TruncDate ,ExtractHour
from orders.models import OrderItem
from foods.models import Category
from .lib import dict_to_list



def get_category_quantity_sold():
    category_quantity_sold = defaultdict(int)
    category_quantity = OrderItem.objects.values('food__category__title').annotate(total_quantity=Sum('quantity'))

    for entry in category_quantity:
        category_name = entry['food__category__title']
        total_quantity = entry['total_quantity']
        category_quantity_sold[category_name] = total_quantity
    return {"new":category_quantity_sold, "old":None}


def category_items():

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

    categories_item = {
            "comparative":{
                "day"  : {"old":{},"new":{}},
                "week" : {"old":{},"new":{}},
                "month": {"old":{},"new":{}},
            },
            "relative":{
                "day"  : {},
                "week" : {},
                "month": {},
            }
        }
    orderitems = OrderItem.objects.all()
    categories = Category.objects.all()
    categories = [i['title'] for i in categories.values('title')]

    for category in categories:
        count_of_category_sold_hour_of_today = []
        for i in range(0,24):
            hour = f'{i}'
            data = orderitems.filter(Q(food__category__title=category) & Q(order__created_at__date=today_date) & Q(order__created_at__hour__gte=i) & Q(order__created_at__hour__lt=i+1))\
            .values('id').annotate(count=Sum('quantity'))
            if data:
                count_of_category_sold_hour_of_today.append(data[0]['count'])
            else:
                count_of_category_sold_hour_of_today.append(0)
        categories_item['comparative']["day"]["new"][category] = sum(count_of_category_sold_hour_of_today)

        count_of_category_sold_hour_of_last_day = []
        for i in range(0,24):
            hour = f'{i}'
            data = orderitems.filter(Q(food__category__title=category) & Q(order__created_at__date=last_day) & Q(order__created_at__hour__gte=i) & Q(order__created_at__hour__lt=i+1))\
            .values('id').annotate(count=Sum('quantity'))
            if data:
                count_of_category_sold_hour_of_last_day.append(data[0]['count'])
            else:
                count_of_category_sold_hour_of_last_day.append(0)
        categories_item['comparative']["day"]["old"][category] = sum(count_of_category_sold_hour_of_last_day)

        categories_item["relative"]["day"][category] = sum(count_of_category_sold_hour_of_last_day)


        count_this_week_category = list(orderitems.filter(Q(food__category__title=category) & Q(order__created_at__date__gte=this_week)).\
        annotate(day=TruncDate('order__created_at')).\
        values('day').annotate(count=Sum('quantity')))
        count_of_category_sold_this_week = dict_to_list(count_this_week_category,value_item='count',thisweek=True)
        categories_item['comparative']["week"]["new"][category] = sum(count_of_category_sold_this_week)


        count_last_week_category =list(orderitems.filter(Q(food__category__title=category) & Q(order__created_at__date__gte=last_week)& Q(order__created_at__date__lt=this_week)).\
        annotate(day=TruncDate('order__created_at')).\
        values('day').annotate(count=Sum('quantity')))
        count_of_category_sold__last_week = dict_to_list(count_last_week_category,value_item='count',lastweek=True)
        categories_item['comparative']["week"]["old"][category] = sum(count_of_category_sold__last_week)


        count_week_category = list(orderitems.filter(Q(food__category__title=category) & Q(order__status='paid') & Q(order__created_at__date__gte=last_7_days)).\
        annotate(day=TruncDate('order__created_at')).\
        values('day').annotate(count=Sum('quantity')))
        count_of_category_sold_for_each_day_of_week = dict_to_list(count_week_category,value_item='count',last7days=True)
        categories_item["relative"]["week"][category] = sum(count_of_category_sold_for_each_day_of_week)


        count_this_month_category = list(orderitems.filter(Q(food__category__title=category) & Q(order__created_at__date__gte=this_month)).\
        annotate(day=TruncDate('order__created_at')).\
        values('day').annotate(count=Sum('quantity')))
        count_of_category_sold_this_month = dict_to_list(count_this_month_category,value_item='count',thismonth=True)
        categories_item['comparative']["month"]["new"][category] = sum(count_of_category_sold_this_month)



        count_last_month_category = list(orderitems.filter(Q(food__category__title=category)& Q(order__created_at__date__gte=last_month)& Q(order__created_at__date__lt=this_month)).\
        annotate(day=TruncDate('order__created_at')).\
        values('day').annotate(count=Sum('quantity')))
        count_of_category_sold_last_month = dict_to_list(count_last_month_category,value_item='count',lastmonth=True)
        categories_item['comparative']["month"]["old"][category] = sum(count_of_category_sold_last_month)


        count_month_category = list(orderitems.filter(Q(food__category__title=category) & Q(order__created_at__date__gte=last_30_days)).\
        annotate(day=TruncDate('order__created_at')).\
        values('day').annotate(count=Sum('quantity')))
        count_of_category_sold_for_each_day_of_month = dict_to_list(count_month_category,value_item='count',last30days=True)
        categories_item["relative"]["month"][category] = sum(count_of_category_sold_for_each_day_of_month)

    return categories_item
