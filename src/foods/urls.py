from django.urls import path
from .views import category_list, food_details , search , category_details

urlpatterns = [
    path("categories/", category_list, name="category_list"),
    path("categories/<int:pk>/", category_details, name="category_details"),
    path("food_details/<int:pk>/", food_details, name="food_details"),
    path("search/", search, name="search"),
]
