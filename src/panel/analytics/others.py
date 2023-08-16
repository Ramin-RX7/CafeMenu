from django.db.models import Count

from datetime import timedelta,datetime

from orders.models import Order
from users.models import User



def user_order_counts(days_back):
    start_date = datetime.now() - timedelta(days=days_back)
    user_order_counts = User.objects.filter(order__created_at__gte=start_date).annotate(order_count=Count('order')).values('phone', 'order_count')
    return {user['phone']: user['order_count'] for user in user_order_counts}


def order_status_counts(days_back):
    start_date = datetime.now() - timedelta(days=days_back)
    status_counts = Order.objects.filter(created_at__gte=start_date).values('status').annotate(count=Count('status'))
    status_count_dict = {item['status']: item['count'] for item in status_counts}
    return status_count_dict
