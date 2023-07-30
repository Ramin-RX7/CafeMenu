from django.urls import path

from .views import *


app_name = "foods"


urlpatterns = [
    path("categories/", category_list, name="category_list"),
    path("categories/<int:id>/", category_details, name="category_details"),
    path("food_details/<int:id>/", food_details, name="food_details"),
    path("search/", search, name="search"),
]
