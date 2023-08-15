import calendar
from datetime import datetime,timedelta
from collections import defaultdict

from django.db.models import Sum,F,Count

from orders.models import Order,OrderItem



ALL_ORDERS = Order.objects.all()



def sales_rel_week():
    today = datetime.now()
    start_date = today - timedelta(days=7)

    orders_within_last_7_days = ALL_ORDERS.filter(status="Paid",created_at__range=(start_date, today))
    amount_sold_by_day = [0] * 7

    for order in orders_within_last_7_days:
        days_ago = (today - order.created_at).days
        if 0 <= days_ago < 7:
            amount_sold_by_day[days_ago] += float(order.price)

    return amount_sold_by_day[::-1]


def sales_rel_day():
    today = datetime.now()
    start_date = today - timedelta(days=1)

    orders_within_last_day = ALL_ORDERS.filter(created_at__range=(start_date, today))
    amount_sold_by_hour = [0] * 24

    for order in orders_within_last_day:
        hours_ago = (today - order.created_at).seconds // 3600
        if 0 <= hours_ago < 24:
            amount_sold_by_hour[hours_ago] += float(order.price)

    return amount_sold_by_hour[::-1]



def sales_rel_month():
    today = datetime.now()
    start_date = today - timedelta(days=30)

    orders_within_last_30_days = ALL_ORDERS.filter(created_at__range=(start_date, today))
    amount_sold_by_day = [0] * 30

    for order in orders_within_last_30_days:
        days_ago = (today - order.created_at).days
        if 0 <= days_ago < 30:
            amount_sold_by_day[days_ago] += float(order.price)

    return amount_sold_by_day[::-1]


def sales_rel_year():
    today = datetime.now()
    start_date = today - timedelta(days=365)

    orders_within_last_year = ALL_ORDERS.filter(created_at__range=(start_date, today))
    amount_sold_by_month = [0] * 12

    for order in orders_within_last_year:
        months_ago = (today.year - order.created_at.year) * 12 + today.month - order.created_at.month
        if 0 <= months_ago < 12:
            amount_sold_by_month[months_ago] += float(order.price)

    return amount_sold_by_month[::-1]




def sales_compar_day():
    def calculate_sales_for_day(day, include_full_day=False):
        start_of_day = day.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = day.replace(hour=23, minute=59, second=59, microsecond=999999)
        orders_within_day = ALL_ORDERS.filter(created_at__range=(start_of_day, end_of_day))
        sales_by_hour = [0] * 24

        for order in orders_within_day:
            hour = order.created_at.hour
            sales_by_hour[hour] += float(order.price)

        if not include_full_day:
            hours_passed = (day - start_of_day).seconds // 3600
            for i in range(hours_passed + 1, 24):
                sales_by_hour[i] = 0

        return sales_by_hour#[::-1]

    now = datetime.now()
    yesterday = now - timedelta(days=1)

    sales_today = calculate_sales_for_day(now)
    sales_yesterday = calculate_sales_for_day(yesterday, include_full_day=True)

    return {"new":sales_today, "old":sales_yesterday}


def sales_compar_week():
    def calculate_sales_for_week(start_of_week, end_of_week):
        orders_within_week = ALL_ORDERS.filter(created_at__range=(start_of_week, end_of_week))
        sales_by_day = [0] * 7

        for order in orders_within_week:
            day_of_week = order.created_at.weekday()
            sales_by_day[day_of_week] += float(order.price)

        return sales_by_day#[::-1]

    now = datetime.now()
    current_week_start = now - timedelta(days=now.weekday())
    current_week_end = current_week_start + timedelta(days=6)

    # Previous week's dates
    previous_week_start = current_week_start - timedelta(weeks=1)
    previous_week_end = current_week_end - timedelta(weeks=1)

    sales_current_week = calculate_sales_for_week(current_week_start, now)
    sales_previous_week = calculate_sales_for_week(previous_week_start, previous_week_end)

    return {"new":sales_current_week, "old":sales_previous_week}


def sales_compar_month():
    def calculate_sales_for_month(year, month, last_day):
        start_of_month = datetime(year, month, 1)
        end_of_month = datetime(year, month, last_day)
        orders_within_month = ALL_ORDERS.filter(created_at__range=(start_of_month, end_of_month))
        sales_by_day = [0] * last_day

        for order in orders_within_month:
            day_of_month = order.created_at.day - 1  # Subtract 1 to get 0-based index
            sales_by_day[day_of_month] += float(order.price)

        return sales_by_day

    now = datetime.now()
    current_year = now.year
    current_month = now.month

    # Previous month's dates
    previous_month_year = current_year if current_month > 1 else current_year - 1
    previous_month = current_month - 1 if current_month > 1 else 12
    previous_month_last_day = (now - timedelta(days=now.day)).day

    current_month_last_day = (now.replace(day=1) + timedelta(days=-1)).day

    sales_current_month = calculate_sales_for_month(current_year, current_month, current_month_last_day)
    sales_previous_month = calculate_sales_for_month(previous_month_year, previous_month, previous_month_last_day)

    return {"new":sales_current_month, "old":sales_previous_month}


def sales_compar_year():
    def calculate_sales_for_year(year, current_month):
        sales_by_month = [0] * 12

        for month in range(1, current_month + 1):
            last_day_of_month = calendar.monthrange(year, month)[1]
            start_of_month = datetime(year, month, 1)
            if month == current_month:
                end_of_month = datetime(year, month, datetime.now().day)
            else:
                end_of_month = datetime(year, month, last_day_of_month)

            orders_within_month = ALL_ORDERS.filter(created_at__range=(start_of_month, end_of_month))
            month_total_sales = sum(float(order.price) for order in orders_within_month)
            sales_by_month[month - 1] = month_total_sales

        return sales_by_month

    now = datetime.now()
    current_year = now.year
    current_month = now.month

    # Previous year
    previous_year = current_year - 1

    sales_current_year = calculate_sales_for_year(current_year, current_month)
    sales_previous_year = calculate_sales_for_year(previous_year, 12)

    return {"new":sales_current_year, "old":sales_previous_year}



def sales_by_category():
    ...




def get_category_quantity_sold():
    category_quantity_sold = defaultdict(int)
    category_quantity = OrderItem.objects.values('food__category__title').annotate(total_quantity=Sum('quantity'))

    for entry in category_quantity:
        category_name = entry['food__category__title']
        total_quantity = entry['total_quantity']
        category_quantity_sold[category_name] = total_quantity

    return {"old":category_quantity_sold}



def get_most_popular_item():
    top_favorite_items = OrderItem.objects.values('food__title').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
    favorite_items_dict = {favorite_item['food__title']: favorite_item['total_quantity'] for favorite_item in top_favorite_items}
    return {"old":favorite_items_dict}


