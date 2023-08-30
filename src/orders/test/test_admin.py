from django.contrib import admin
from django.test import TestCase, RequestFactory, Client
from orders.admin import OrderToDayFilter, OrderStatusFilter, OrderAdmin, TableAdmin
from orders.models import Order
from unittest.mock import Mock
from django.contrib.admin import SimpleListFilter
from datetime import datetime, timedelta
from django.contrib.admin.sites import AdminSite
from django.contrib.admin import ModelAdmin
from orders.models import Table, Order, OrderItem
from users.models import User 
from django.urls import reverse
from django.db.models.query import QuerySet

class TestAdmin(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.model_admin = ModelAdmin(Order, self.site)
        self.order_admin = OrderAdmin(Order, self.site)
        self.table_admin = TableAdmin(Table, self.site)
        self.filter = OrderToDayFilter(None, {'Date': 'todaye'}, self.model_admin, self.site)
        self.factory = RequestFactory()
        self.client = Client()
        
        self.table1 = Table.objects.create(
            name='table 1',
            is_reserved=False,
        )
        
        self.user1 = User.objects.create(
            phone="9176877108",
            first_name = 'Ali',
            last_name= 'Afzal',
            is_active=True,
            is_staff=False,
        )
        
        
    def test_lookups_order_detail_filter(self):
            filter_instance = OrderToDayFilter(
                request=None,
                params={},
                model=Order,
                model_admin=None 
            )
            
            expected_lookups = [('today', 'today')]
            self.assertEqual(filter_instance.lookups(None, None), expected_lookups)
        

    def test_lookups_order_staus_filter(self):
        filter_instance = OrderStatusFilter(
            request=None,
            params={},
            model=Order,
            model_admin=None
        )
        
        expected_lookups = [('not_paid', 'not_paid')]
        self.assertEqual(filter_instance.lookups(None, None), expected_lookups)

    def test_list_display_order_admin(self):
        self.assertEqual(
            self.order_admin.list_display,
            ['customer', 'table', 'status', 'price', 'discount', 'final_price', 'created_at']
        )
        
    def test_ordering_order_admin(self):
        self.assertEqual(self.order_admin.ordering, ['created_at', 'updated_at'])
        
    def test_list_filter_order_admin(self):
        self.assertEqual(
            self.order_admin.list_filter,
            [OrderToDayFilter, OrderStatusFilter]
        )
        
    def test_list_per_page_order_admin(self):
        self.assertEqual(self.order_admin.list_per_page, 20)
        
    def test_readonly_fields_order_admin(self):
        self.assertEqual(self.order_admin.readonly_fields, ["created_at"])
        
    def test_list_display_table_admin(self):
        self.assertEqual(
            self.table_admin.list_display,
            ['name', 'is_reserved']
        )
        
    def test_queryset_order_today_filter(self):
        mock_request = Mock()  
        mock_model_admin = Mock()  

        today = datetime.today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        
        orders = [
            Order(
            customer='9176877108',
            table=self.table1,
            discount=2,
            responsible_staff=self.user1,
            created_at=yesterday,
                ),
            Order(
            customer='9176877107',
            table=self.table1,
            discount=2,
            responsible_staff=self.user1,
            created_at=today,
                ),
            Order(
            customer='9176877109',
            table=self.table1,
            discount=2,
            responsible_staff=self.user1,
            created_at=tomorrow,
                ),
        ]
        
        queryset = QuerySet(model=Order, query=None, using='default')
        queryset._result_cache = orders  
        
        filter_instance = OrderToDayFilter(
            request=mock_request,
            params={'Date': 'today'},
            model=Order,
            model_admin=mock_model_admin
        )

        filtered_queryset = filter_instance.queryset(mock_request, queryset)
        # print(filtered_queryset)
        self.assertEqual(len(filtered_queryset), 0)
        
        for order in orders:
            if order.created_at.date() != today.date():
                self.assertNotIn(order, filtered_queryset)