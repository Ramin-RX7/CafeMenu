from django.urls import path
from .views import *


app_name = "orders"


urlpatterns = [
    path("order_list/", order_list, name="order_list"),
    path("<int:id>/", order_details, name="order_details"),
    path("cart/", cart, name="cart"),
    path("", index, name="index"),
    path("cart/delete/",cart_delete,name="cart_delete"),
    path("customer_login/", customer_login,name="customer_login"),
    path("cart_add/", cart_add, name='cart_add'),
    path("set/", SetOrderView.as_view(), name="set_order"),
]
