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



