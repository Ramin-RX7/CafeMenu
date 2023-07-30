from django.urls import path
from .views import order_list, order_details, customer_login

urlpatterns = [
    path("order_list/", order_list, name="order_list"),
    path("order_details/", order_details, name="order_details"),
    path("customer_login/", customer_login,name="customer_login"),
]
