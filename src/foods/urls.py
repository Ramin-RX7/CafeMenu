from django.urls import path

from .views import *


app_name = "foods"


urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("category/<int:id>/", CategoryDetailView.as_view(), name="category_details"),
    path("search/", SearchView.as_view(), name="search"),
    path("<int:id>/", FoodDetailView.as_view(), name="food_details"),
    path("menu/", menu, name="menu")
]
