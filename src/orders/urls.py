from django.urls import path
from .views import order_list, order_details,cart

urlpatterns = [
    path("order_list/", order_list, name="order_list"),
    path("order_details/<int:id>", order_details, name="order_details"),
    path("cart/",cart, name="cart"),
]