from django.test import TestCase
from django.urls import reverse
from foods.models import Category,Food


class FoodsViewTest(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(
            # id = 1,
            title = "category test",
            description ="Category descriptoin test"
        )
        
        self.food = Food.objects.create(
            # id = 1,
            title = "test food",
            description ="food descriptoin test",
            price = 10,
            category = self.category,
            is_active =False
        )
        
        self.category_list_url=reverse("foods:category_list")
        self.category_detail_url=reverse("foods:category_details",kwargs={'id':self.category.id})
        self.food_detail_url=reverse("foods:food_details",kwargs={'id':self.food.id})
        self.search_url=reverse("foods:search")
        self.menu_list_url=reverse("foods:menu")
            
    def test_category_list_view(self):
        resp = self.client.get(self.category_list_url)
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,'foods/category_list.html')
        
    def test_category_detail_view(self):
        resp = self.client.get(self.category_detail_url)
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,'foods/category_details.html')
        
    def test_food_detail_view(self):
        resp = self.client.get(self.food_detail_url)
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,"foods/food_details.html")
        
    def test_search_view(self):
        resp = self.client.get(self.search_url,{'searched':'tes'})
        self.assertEqual(Food.objects.filter(title__contains='tes').count(),1)
        self.assertEqual(Food.objects.filter(title__contains='ramin').count(),0)
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,'foods/search.html')
        
        
    def test_menu_view(self):
        resp = self.client.get(self.menu_list_url)
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,'foods/menu.html')