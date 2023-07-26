from django.urls import path
from .views import category_list, food_details

urlpatterns = [
    path("categories/", category_list, name="category_list"),
    path("food_details/<int:pk>/", food_details, name="food_details"),
]
