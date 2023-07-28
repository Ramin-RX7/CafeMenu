from django.urls import path
from .views import order_list, order_details

urlpatterns = [
    path("order_list/", order_list, name="order_list"),
    path("order_details/<int:pk>", order_details, name="order_details"),
]