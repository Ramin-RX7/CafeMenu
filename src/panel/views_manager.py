import json
from datetime import timedelta,datetime

from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.db.models import Sum

from orders.models import OrderItem

from .analytics import *




def json_api(request):
    context = {
        "sales": {
            "comparative":{
                "day" :  sales_compar_day(),
                "week":  sales_compar_week(),
                "month": sales_compar_month(),
                "year":  sales_compar_year(),
            },
            "relative": {
                "day": sales_rel_day(),
                "week": sales_rel_week(),
                "month": sales_rel_month(),
                "year": sales_rel_year(),
            }
        },

        "items":{
            **food_items()
            # "comparative": {
            #     **get_top_selling_items()
            # },
            # "relative":{
            #     "total": get_most_popular_item()
            # }
        },

        "orders": {**count_orders()},

        "categories": {
            "comparative": {
                "total": get_category_quantity_sold(),
            }
        },
        "customer-sales":{
            "relative": {
                "week":  customerSales_rel(7),
                "month": customerSales_rel(30),
                "year":  customerSales_rel(365),
            }
        },
        "unique-customers": {
            "relative": {
                "week": unique_customers_rel(7),
                "month": unique_customers_rel(30),
            }
        },
        "others":{
            "relative" : {
                "peak-hour": get_peak_hours(),
                "staff-orders-week": {"new":user_order_counts(7), "old":None},
                "staff-orders-month": {"new":user_order_counts(30), "old":None},
                "order-status-week": {"new":order_status_counts(7), "old":None},
                "order-status-month": {"new":order_status_counts(30), "old":None},
            }
        }
    }
    return HttpResponse(json.dumps(context))



def analytics(request):
    context = {
        "peak_hours": get_top_peak_hours(),
        "sales_total":sales_total(),
    }
    return render(request, "panel/dashboard_manager.html", context)
