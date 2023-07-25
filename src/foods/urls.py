from django.urls import path
from .views import category_list, food_details,home

urlpatterns = [
    path('', home, name="home"),
    path("categories/", category_list, name="category_list"),
    path("food_details/", food_details, name="food_details"),
]
