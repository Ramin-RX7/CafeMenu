from django.test import TestCase, Client
from django.urls import reverse
from foods.models import Category, Food
from foods.forms import CategoryForm, FoodForm
from django.contrib.admin import SimpleListFilter
from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from foods.admin import FoodAdmin,FoodFilter,CategoryFilter
User=get_user_model()

class FoodFilterTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.filter1 = FoodFilter(
            request=None,
            params={'Active':'inactive'},
            model=Food,
            model_admin=FoodAdmin,
        )
        self.filter2 = FoodFilter(
            request=None,
            params={'Active':None},
            model=Food,
            model_admin=FoodAdmin,
        )
        self.category=Category.objects.create(title='test')

    def test_lookups(self):
        expected_lookups = [('inactive', 'inactive')]
        lookups = self.filter1.lookups(None, None)
        self.assertEqual(lookups, expected_lookups)

    def test_queryset_with_inactive(self):
        user = User.objects.create_user(phone='09123456789',password="admin")
        food1 = Food.objects.create(title='Food 1', is_active=True,price=7 ,category=self.category)
        food2 = Food.objects.create(title='Food 2', is_active=False,price=7,category=self.category)
        request = self.client.get('/admin/foods/food/')
        queryset1 = Food.objects.all()
        filtered_queryset = self.filter1.queryset(request, queryset1)
        self.assertQuerysetEqual(filtered_queryset,[food2.pk], transform=lambda x: x.pk)

    def test_queryset_without_inactive(self):
        user = User.objects.create_user(phone='09123456789', password='admin')
        food1 = Food.objects.create(title='Food 1', is_active=True ,price=7,category=self.category)
        food2 = Food.objects.create(title='Food 2', is_active=False ,price=7,category=self.category)
        request = self.client.get('/admin/foods/food/')
        queryset1 = Food.objects.all()
        filtered_queryset = self.filter2.queryset(request, queryset1)
        self.assertEqual(filtered_queryset,None)


class CategoryFilterTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.filter1 = CategoryFilter(
            request=None,
            params={'title': 'title'},
            model=Food,
            model_admin=None,
        )
        self.filter2 = CategoryFilter(
            request=None,
            params={},
            model=Food,
            model_admin=None,
        )

    def test_lookups(self):
        expected_lookups = [('title', 'Categories')]
        lookups = self.filter1.lookups(None, None)
        self.assertEqual(lookups, expected_lookups)

    def test_queryset_with_title_filter(self):
        category1 = Category.objects.create(title='category1')
        category2 = Category.objects.create(title='category2')
        food1 = Food.objects.create(title='Food 1', is_active=True,price=7 ,category=category1)
        food2 = Food.objects.create(title='Food 2', is_active=True,price=7 ,category=category1)
        food3 = Food.objects.create(title='Food 3', is_active=True,price=7 ,category=category1)

        request = self.client.get('/admin/foods/category/')
        queryset = Category.objects.all()
        filtered_queryset = self.filter1.queryset(request, queryset)
        self.assertQuerysetEqual(filtered_queryset, [category2.pk], transform=lambda x: x.pk)

    def test_queryset_without_title_filter(self):
        category1 = Category.objects.create(title='category1')
        category2 = Category.objects.create(title='category2')
        food1 = Food.objects.create(title='Food 1', is_active=True,price=7 ,category=category1)
        food2 = Food.objects.create(title='Food 2', is_active=True,price=7 ,category=category1)
        food3 = Food.objects.create(title='Food 3', is_active=True,price=7 ,category=category1)

        request = self.client.get('/admin/foods/category/')
        queryset = Category.objects.all()
        filtered_queryset = self.filter2.queryset(request, queryset)
        self.assertEqual(filtered_queryset,None)