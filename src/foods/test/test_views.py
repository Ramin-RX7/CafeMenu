from django.test import TestCase
from django.urls import reverse
from foods.models import Category,Food
from foods.views import MenuListView


class FoodsViewTest(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(
            # id = 1,
            title = "category test",
            description ="Category descriptoin test"
        )
        self.category2 = Category.objects.create(
            # id = 1,
            title = "category test2",
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
        self.food2 = Food.objects.create(
            # id = 1,
            title = "test food2",
            description ="food descriptoin test",
            price = 10,
            category = self.category2,
            is_active =False
        )
        self.food3 = Food.objects.create(
            # id = 1,
            title = "test food3",
            description ="food descriptoin test",
            price = 10,
            category = self.category2,
            is_active =False
        )
        
        self.category_list_url=reverse("foods:category_list")
        self.category_detail_url=reverse("foods:category_details",kwargs={'id':self.category2.id})
        self.food_detail_url=reverse("foods:food_details",kwargs={'id':self.food2.id})
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
        self.assertEqual(Food.objects.filter(title__contains='tes').count(),3)
        self.assertEqual(Food.objects.filter(title__contains='ramin').count(),0)
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,'foods/search.html')


    # def test_menu_view(self):
    #     resp = self.client.get(self.menu_list_url)
    #     self.assertEqual(resp.status_code,200)
    #     self.assertTemplateUsed(resp,'foods/menu.html')

    def test_menulist(self):
        view = MenuListView()
        queryset = view.get_queryset()
    
        self.assertQuerysetEqual(
            queryset,
            [self.category.pk, self.category2.pk],
            transform = lambda x: x.pk
        )

        for category in queryset:
            self.assertGreater(category.num_foods, 0)
            self.assertTrue(hasattr(category, 'food_set'))
            
    def test_categorylist(self):
        response = self.client.get(self.category_list_url)
        view = response.context['view']
        queryset = view.get_queryset()
        self.assertEqual(len(queryset),2)
        
    def test_categorydetail(self):
        response = self.client.get(self.category_detail_url)
        view = response.context['view']
        context = view.get_context_data()

        self.assertEqual(context['category'], self.category2)
        self.assertEqual(len(context['foods']),2)
        
    def test_fooddetail(self):
        response = self.client.get(self.food_detail_url)
        view = response.context['view']
        context = view.get_context_data()
        self.assertEqual(context['food'],self.food2)