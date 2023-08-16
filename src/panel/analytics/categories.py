from collections import defaultdict

from django.db.models import Sum

from orders.models import OrderItem



def get_category_quantity_sold():
    category_quantity_sold = defaultdict(int)
    category_quantity = OrderItem.objects.values('food__category__title').annotate(total_quantity=Sum('quantity'))

    for entry in category_quantity:
        category_name = entry['food__category__title']
        total_quantity = entry['total_quantity']
        category_quantity_sold[category_name] = total_quantity
    return {"new":category_quantity_sold, "old":None}
