from django.urls import path

from .views import *



app_name = "panel"



authentication_urls = [
    path('login/', LoginView.as_view(), name='login'),
    path('send-otp/', SendOTPView.as_view(), name="send-otp"),
    path('logout/', logout, name="logout"),
]


dashboard_urls = [
    path("order/<int:order_id>/edit/", EditOrders.as_view(), name="edit_order"),
    path("order/<int:order_id>/approve/", approve_order, name="approve_order"),
    path("order/<int:order_id>/reject/", reject_order, name="reject_order"),
    path("order/<int:order_id>/pay/", pay_order, name="pay_order"),
    path("order/<int:order_id>/deliver/", deliver_order, name="deliver_order"),
    path("order/<int:order_id>/take/", take_responsibility, name="take_responsibility"),
    path("",dashboard, name="dashboard"),
]


analytics_urls = [
    path("analytics-api/", JsonAPI.as_view(), name="analytics-api"),
    path("analytics/", analytics, name="analytics"),
    path("download/<str:dataset_name>", download_dataset, name="dataset_download"),
]



urlpatterns = [
    *authentication_urls,
    *analytics_urls,
    *dashboard_urls
]
