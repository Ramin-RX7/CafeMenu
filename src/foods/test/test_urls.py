from django.test import SimpleTestCase
from django.urls import reverse,resolve
from foods.views import FoodDetailView,CategoryDetailView,CategoryListView,MenuListView,SearchView


class TestUrls(SimpleTestCase):
            
    def test_list_menu(self):
        url=reverse("foods:menu")
        self.assertEquals(resolve(url).func.view_class,MenuListView)
    
    def test_list_category_list(self):
        url=reverse("foods:category_list")
        self.assertEquals(resolve(url).func.view_class,CategoryListView)   
        
    def test_list_category_details(self):
        url=reverse("foods:category_details",kwargs={'id':1})
        self.assertEquals(resolve(url).func.view_class,CategoryDetailView)
        
    def test_list_food_details(self):
        url=reverse("foods:food_details",kwargs={'id':2})
        self.assertEquals(resolve(url).func.view_class,FoodDetailView)
        
    def test_list_searh(self):
        url=reverse("foods:search")
        self.assertEquals(resolve(url).func.view_class,SearchView)