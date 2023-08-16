from datetime import timedelta,datetime

from django.db.models import Count,F
from django.db.models.functions import ExtractHour

from orders.models import Order



def get_peak_hours():
    orders_with_hour = Order.objects.annotate(created_hour=F('created_at__hour'))
    hourly_order_counts = orders_with_hour.values('created_hour').annotate(order_count=Count('id')).order_by('-order_count')[:5]
    peak_hours_dict = {hourly_order['created_hour']: hourly_order['order_count'] for hourly_order in hourly_order_counts}
    return ({"new":peak_hours_dict, "old":None})


def get_top_peak_hours():
    now = datetime.now()
    month = now.month
    year = now.year

    start_date = datetime(year, month, 1)
    end_date = start_date.replace(month=month+1) - timedelta(days=1)
    activities_in_month = Order.objects.filter(created_at__range=(start_date, end_date))

    top_hours_in_month = activities_in_month.annotate(hour=ExtractHour('created_at')).values('hour').annotate(count=Count('id')).order_by('-count')[:5]

    top_hours_in_year = Order.objects.filter(created_at__year=year).annotate(hour=ExtractHour('created_at')).values('hour').annotate(count=Count('id')).order_by('-count')[:5]

    response_data = {
        "year": [item['hour'] for item in top_hours_in_year],
        "month": [item['hour'] for item in top_hours_in_month]
    }

    return response_data