from django.test import TestCase, RequestFactory
from orders.admin import OrderToDayFilter, OrderStatusFilter, OrderAdmin, TableAdmin
from orders.models import Order
from unittest.mock import Mock
from django.contrib.admin import SimpleListFilter
from datetime import datetime, timedelta
from django.contrib.admin.sites import AdminSite
from django.contrib.admin import ModelAdmin
from orders.models import Table, Order, OrderItem
from users.models import User 


class TestAdmin(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.model_admin = ModelAdmin(Order, self.site)
        self.order_admin = OrderAdmin(Order, self.site)
        self.table_admin = TableAdmin(Table, self.site)
        self.filter = OrderToDayFilter(None, {'Date': 'todaye'}, self.model_admin, self.site)
        self.factory = RequestFactory()
        
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