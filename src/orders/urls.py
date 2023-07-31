from django.urls import path
from .views import *


app_name = "orders"


urlpatterns = [
    path("order_list/", order_list, name="order_list"),
    path("order/<int:id>/", order_details, name="order_details"),
    path("cart/", cart, name="cart"),
    # path("cart/add/<int:id>", cart_add, name="cart_add"),
    path("", index, name="index"),
    path("cart/delete/",cart_delete,name="cart_delete"),
]