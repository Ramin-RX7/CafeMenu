import json
from datetime import datetime,timedelta

from django.http import Http404
from django.views import View
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from dynamic_menu.models import Configuration
from ..analytics.datasets import *
from ..analytics import *




datasets = {
    "orderitems" : export_order_items_to_csv,
    "orders" : export_orders_to_csv,
}



def download_dataset(request, dataset_name):
    if dataset_name in datasets:
        return datasets[dataset_name](request)
    else:
        raise Http404



@permission_required("analytics", raise_exception=True)
def analytics(request):
    context = {
        "peak_hours": get_top_peak_hours(),
        "sales_total":sales_total(),
        "datasets": datasets.keys()
    }
    return render(request, "panel/analytics.html", context)



def get_analytics_data():
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



class JsonAPI(PermissionRequiredMixin, View):
    permission_required = ("analytics",)

    _conf = None
    last_update = datetime.now()
    current_data = None
    @property
    def configurations(self):
        if not self._conf:
            self._conf = Configuration.objects.first()
        return self._conf


    def get(self, request):
        if self.last_update + timedelta(hours=self.configurations.analytics_refresh)  <  datetime.now():
            self.current_data = get_analytics_data()
            self.last_update = datetime.now()
        return self.current_data
