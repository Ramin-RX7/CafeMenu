from django.urls import path

from .views import *


urlpatterns = [
    path("about/", about_us, name="about_us"),
    path("", index, name="index"),
]