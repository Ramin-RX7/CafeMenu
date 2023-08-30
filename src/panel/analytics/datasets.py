import csv
from django.http import HttpResponse

from orders.models import OrderItem



def export_order_items_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order_items.csv"'

    order_items = OrderItem.objects.all()

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Customer', 'Food', 'Quantity', 'Unit Price', 'Discount'])

    for order_item in order_items:
        writer.writerow([order_item.order.id, order_item.order.customer, order_item.food.title, order_item.quantity,
                         order_item.unit_price, order_item.discount])

    return response


def export_orders_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order_items.csv"'

    order_items = OrderItem.objects.all()

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Customer', 'Food', 'Quantity', 'Unit Price', 'Discount'])

    for order_item in order_items:
        writer.writerow([order_item.order.id, order_item.order.customer, order_item.food.title, order_item.quantity,
                         order_item.unit_price, order_item.discount])

    return response
