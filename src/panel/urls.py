from django.urls import path
from .views import *


app_name = "panel"


urlpatterns = [
    path("",dashboard_staff, name="dashboard"),
    path("order/<int:order_id>/edit/", EditOrders.as_view(), name="edit_order"),
    path("order/<int:order_id>/approve/", approve_order, name="approve_order"),
    path("order/<int:order_id>/reject/", reject_order, name="reject_order"),
    path("order/<int:order_id>/pay/", pay_order, name="pay_order"),
    path("order/<int:order_id>/deliver/", deliver_order, name="deliver_order"),
]