from django.test import TestCase, Client, RequestFactory
from django.urls import reverse, reverse_lazy
from orders.models import Table, Order, OrderItem


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.order_list_url = reverse('orders:order_list')
        self.index = reverse('orders:index')
        
    def test_index_GET(self):
        response = self.client.get(self.order_list_url)
        self.assertEquals(response.status_code, 302)
    
    def test_order_list_GET(self):
        response = self.client.get(self.index)
        self.assertEquals(response.status_code, 200)