from django.urls import path
from .views import *


app_name = "panel"


urlpatterns = [
    path('login', login, name='login'),
    path('verify/', user_verify, name='user_verify')

]