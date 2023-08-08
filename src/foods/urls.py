from django.urls import path

from .views import *


app_name = "foods"


urlpatterns = [
    path("categories/", category_list, name="category_list"),
    path("category/<int:id>/", category_details, name="category_details"),
    path("search/", SearchView.as_view(), name="search"),
    path("<int:id>/", food_details, name="food_details"),
    path("menu/", menu, name="menu")
]
