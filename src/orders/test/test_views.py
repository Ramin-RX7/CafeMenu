from django.test import TestCase, Client, RequestFactory
from django.urls import reverse, reverse_lazy
from orders.models import Table, Order, OrderItem
from orders.views import IndexView, OrderDetailView, SetOrderView
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.order_list_url = reverse('orders:order_list')
        self.index_url = reverse('orders:index')
        self.set_order = reverse('orders:set_order')
        self.cart_url = reverse('orders:cart')
        
        self.view_index = IndexView()
        self.view_order_detail = OrderDetailView()
        self.factory = RequestFactory()
        
        self.category1 = Category.objects.create(
            title='Iranian Foods'
        )
        
        self.food1 = Food.objects.create(
            title='Kabab',
            price=22,
            category=self.category1
        )
        
        
        self.table1 = Table.objects.create(
            name='table 1',
            is_reserved=False,
        )
        
        self.table2 = Table.objects.create(
            name='table 2',
            is_reserved=True,
        )
        
        self.user1 = User.objects.create(
            phone="9176877108",
            first_name = 'Ali',
            last_name= 'Afzal',
            is_active=True,
            is_staff=False,
        )
        
        self.order1 = Order(
            customer='9176877108',
            table=self.table1,
            discount=2,
            responsible_staff=self.user1,
        )
        self.order1.save(check_items=False)
        
        self.order2 = Order(
            customer='9173523513',
            table=self.table2,
            discount=0,
            responsible_staff=self.user1, 
        )
        self.order2.save(check_items=False)