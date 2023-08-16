from collections import defaultdict
from datetime import datetime,timedelta

from django.db.models import Sum

from orders.models import Order



def customerSales_rel(days):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    phone_total_spent = defaultdict(float)
    for order in Order.objects.filter(created_at__range=(start_date, end_date)):
        phone_total_spent[order.customer] += float(order.price)

    sorted_phone_total_spent = sorted(phone_total_spent.items(), key=lambda item: item[1], reverse=True)
    top_customers = {phone: total_spent for phone, total_spent in sorted_phone_total_spent[:5]}

    return {"new":top_customers, "old":None}
