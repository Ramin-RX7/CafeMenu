from django.urls import path
from .views import *


app_name = "orders"


urlpatterns = [
    path("order_list/", order_list, name="order_list"),
    path("<int:id>/", order_details, name="order_details"),
    path("cart/", cart, name="cart"),
    path("", IndexTemplateView.as_view(), name="index"),
    path("cart/delete/",CartDeleteView.as_view(),name="cart_delete"),
    path("customer_login/", CustomerLoginView.as_view(),name="customer_login"),
    path("cart_add/", CartAddView.as_view(), name='cart_add'),
    path("set/", SetOrderView.as_view(), name="set_order"),
]
