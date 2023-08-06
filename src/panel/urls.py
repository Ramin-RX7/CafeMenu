from django.urls import path
from .views import *


app_name = "panel"


urlpatterns = [
    path("",dashboard_staff, name="dashboard_staff")
]