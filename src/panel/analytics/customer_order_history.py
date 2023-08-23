import datetime
from django.db.models import Count, Q
from orders.models import Order
from django.db.models.functions import TruncDate
from .lib import dict_to_list

def customer_order_history(phone):
    all_orders = Order.objects.filter(customer=phone)

    today = datetime.datetime.today()
    last_day = today - datetime.timedelta(1)
    last_7_days = today - datetime.timedelta(7)
    last_30_days = today - datetime.timedelta(30)
    week_start_day = today - datetime.timedelta(today.weekday())
    last_week_start_day = week_start_day - datetime.timedelta(7)
    month_start_day = today.replace(day=1)
    last_month_start_day = (month_start_day - datetime.timedelta(1)).replace(day=1)
    results = {
        "comparative": {
            "day": {"old": [], "new": []},
            "week": {"old": [], "new": []},
            "month": {"old": [], "new": []}
        },
        "relative": {
            "day": [],
            "week": [],
            "month": []
        }
    }

    for i in range(24):
        current_day_hour_count = all_orders.filter(
            created_at__date=today,
            created_at__hour=i
        ).count()
        
        last_day_hour_count = all_orders.filter(
            created_at__date=last_day,
            created_at__hour=i
        ).count()
        
        results['comparative']['day']['new'].append(current_day_hour_count)
        results['comparative']['day']['old'].append(last_day_hour_count)
        results['relative']['day'].append(current_day_hour_count)

    for period, start_date, end_date in [('week', week_start_day, today), 
                                         ('month', month_start_day, today)]:
        current_period_counts = all_orders.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        ).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id'))
        
        last_period_start = start_date - (start_date - end_date)
        last_period_end = start_date
        
        last_period_counts = all_orders.filter(
            created_at__date__gte=last_period_start,
            created_at__date__lt=last_period_end
        ).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id'))

        results['comparative'][period]['new'] = dict_to_list(current_period_counts, 'count')
        results['comparative'][period]['old'] = dict_to_list(last_period_counts, 'count')
        results['relative'][period] = dict_to_list(current_period_counts, 'count')

    return results
