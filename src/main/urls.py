from django.urls import path

from .views import *


urlpatterns = [
    path("about/", AboutUsTemplateView.as_view(), name="about_us"),
    path("", IndexTemplateView.as_view(), name="index"),
]
