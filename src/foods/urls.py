from django.urls import path
from .views import category_list, food_details , search

urlpatterns = [
    path("categories/", category_list, name="category_list"),
    path("food_details/", food_details, name="food_details"),
    path("search/", search, name="search"),
]
