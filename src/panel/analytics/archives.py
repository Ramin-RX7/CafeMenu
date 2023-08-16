from datetime import datetime,timedelta

from django.db.models import Count,Sum

from orders.models import Order,OrderItem



def get_unique_visitors():
    current_time = datetime.now()
    start_of_week = current_time - timedelta(days=current_time.weekday())
    start_of_month = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_of_year = current_time.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    def calculate_data(queryset):
        return queryset.values('created_at__hour').annotate(count=Count('customer')).order_by('created_at__hour')

    comparative_data = {
        "day": {
            "old": calculate_data(Order.objects.filter(created_at__date=current_time - timedelta(days=1))),
            "new": calculate_data(Order.objects.filter(created_at__date=current_time))
        },
        "week": {
            "old": calculate_data(Order.objects.filter(created_at__date__range=[start_of_week - timedelta(days=7), start_of_week - timedelta(days=1)])),
            "new": calculate_data(Order.objects.filter(created_at__date__range=[start_of_week, current_time]))
        },
        "month": {
            "old": calculate_data(Order.objects.filter(created_at__date__range=[start_of_month - timedelta(days=30), start_of_month - timedelta(days=1)])),
            "new": calculate_data(Order.objects.filter(created_at__date__range=[start_of_month, current_time]))
        },
        "year": {
            "old": calculate_data(Order.objects.filter(created_at__date__range=[start_of_year - timedelta(days=365), start_of_year - timedelta(days=1)])),
            "new": calculate_data(Order.objects.filter(created_at__date__range=[start_of_year, current_time]))
        }
    }

    response_data = {
        "comparative": comparative_data,
    }

    return response_data



def get_most_popular_item():
    top_favorite_items = OrderItem.objects.values('food__title').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
    favorite_items_dict = {favorite_item['food__title']: favorite_item['total_quantity'] for favorite_item in top_favorite_items}
    return {"new":favorite_items_dict, "old":None}



# Get top 10 selling items (most items sold) in day, week, month, year
def get_top_selling_items():
    current_time = datetime.now()
    start_of_day = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_week = current_time - timedelta(days=current_time.weekday())
    start_of_month = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_of_year = current_time.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    top_selling_in_day = OrderItem.objects.filter(created_at__gte=start_of_day).values('food__title').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:10]
    top_selling_in_week = OrderItem.objects.filter(created_at__gte=start_of_week).values('food__title').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:10]
    top_selling_in_month = OrderItem.objects.filter(created_at__gte=start_of_month).values('food__title').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:10]
    top_selling_in_year = OrderItem.objects.filter(created_at__gte=start_of_year).values('food__title').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:10]

    top_selling_data = {
        "day"  : {"new": {item['food__title']:item['total_quantity'] for item in top_selling_in_day  }, "old":None},
        "week" : {"new": {item['food__title']:item['total_quantity'] for item in top_selling_in_week }, "old":None},
        "month": {"new": {item['food__title']:item['total_quantity'] for item in top_selling_in_month}, "old":None},
        "year" : {"new": {item['food__title']:item['total_quantity'] for item in top_selling_in_year }, "old":None},
    }

    return top_selling_data


# Get 10 phone numbers that has the most money spend in our cafe in week,month,year
def get_top_spending_customers():
    current_time = datetime.now()
    start_of_week = current_time - timedelta(days=current_time.weekday())
    start_of_month = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_of_year = current_time.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    top_spending_in_week = OrderItem.objects.filter(created_at__gte=start_of_week).values('order__customer').annotate(total_spent=Sum('unit_price')).order_by('-total_spent')[:10]
    top_spending_in_month = OrderItem.objects.filter(created_at__gte=start_of_month).values('order__customer').annotate(total_spent=Sum('unit_price')).order_by('-total_spent')[:10]
    top_spending_in_year = OrderItem.objects.filter(created_at__gte=start_of_year).values('order__customer').annotate(total_spent=Sum('unit_price')).order_by('-total_spent')[:10]

    top_spending_customers_data = {
        "year": {"new": [item['order__customer'] for item in top_spending_in_year] , "old":None},
        "month":{"new": [item['order__customer'] for item in top_spending_in_month], "old":None},
        "week": {"new": [item['order__customer'] for item in top_spending_in_week] , "old":None}
    }

    return top_spending_customers_data
