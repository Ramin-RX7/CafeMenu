from collections import defaultdict
from datetime import datetime,timedelta

from orders.models import Order


def unique_customers_rel(days):
    unique_customers_by_day = defaultdict(set)

    for day in range(days):
        end_date =   datetime.now() - timedelta(days=day)
        start_date = datetime(end_date.year, end_date.month, end_date.day, 0, 0, 0)
        end_date =   datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)

        unique_customers = Order.objects.filter(created_at__range=(start_date, end_date)).values('customer').distinct()

        unique_customers_by_day[day] = len(unique_customers)

    return list(unique_customers_by_day.values())[::-1]
