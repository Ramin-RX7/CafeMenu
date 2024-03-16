from django.urls import path
from .views import *


app_name = "orders"


urlpatterns = [
    path("order_list/", OrderListView.as_view(), name="order_list"),
    path("<int:id>/", OrderDetailView.as_view(), name="order_details"),
    path("cart/", cart, name="cart"),
    path("", IndexView.as_view(), name="index"),
    path("set/", SetOrderView.as_view(), name="set_order"),
]
