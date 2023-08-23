from django.test import Client, TestCase
from django.urls import reverse_lazy, resolve, reverse
from orders.views import OrderListView, IndexView, OrderDetailView, SetOrderView, CartAddView, CartDeleteView, CustomerLoginView, cart
from orders.models import Table, Order
from users.models import User
from django.test.client import RequestFactory

class TestUrls(TestCase):
    def setUp(self):
        self.client = Client()
        self.order_list_url = reverse('orders:order_list')
        self.cart_url = reverse('orders:cart')
        self.index_url = reverse('orders:index')
        self.cart_delete_url = reverse('orders:cart_delete')
        self.customer_login_url = reverse('orders:customer_login')
        self.cart_add_url = reverse('orders:cart_add')
        self.set_order_url = reverse('orders:set_order')
        
        self.factory = RequestFactory()
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
        
        self.order1 = Order(
            customer='9176877108',
            table=self.table1,
            discount=2,
            responsible_staff=self.user1,
        )
        self.order1.save(check_items=False)
        
    def test_order_list_url_status_code(self):
            response = self.client.get(self.order_list_url)
            self.assertEquals(response.status_code, 302)
            
    def test_order_details_url__status_code(self):
        request = self.factory.get(reverse('orders:order_details', args=[self.order1.id]))
        self.client.login(phone="9176877108" ,first_name="Ali")
        response = self.client.get(request)
        self.assertEqual(response.status_code, 404)
    
    def test_cart_url_status_code(self):
            response = self.client.get(self.cart_url)
            self.assertEquals(response.status_code, 200)
    
    def test_index_url_status_code(self):
            response = self.client.get(self.index_url)
            self.assertEquals(response.status_code, 200)
    
    def test_customer_login_url_status_code(self):
            response = self.client.post(self.customer_login_url)
            self.assertEquals(response.status_code, 302)
            
    def test_set_order_url_status_code(self):
            response = self.client.get(self.set_order_url)
            self.assertEquals(response.status_code, 405)
            
    def test_order_list_url_is_resolved(self):
        url =reverse_lazy('orders:order_list')
        self.assertEquals(resolve(url).func.view_class, OrderListView)
        
    def test_cart_url_is_resolved(self):
        url =reverse_lazy('orders:cart')
        self.assertEquals(resolve(url).func, cart)
    
    def test_index_url_is_resolved(self):
        url =reverse_lazy('orders:index')
        self.assertEquals(resolve(url).func.view_class, IndexView)
        
    def test_cart_delete_url_is_resolved(self):
        url =reverse_lazy('orders:cart_delete')
        self.assertEquals(resolve(url).func.view_class, CartDeleteView)
        
    def test_customer_login_url_is_resolved(self):
        url =reverse_lazy('orders:customer_login')
        self.assertEquals(resolve(url).func.view_class, CustomerLoginView)
        
    def test_cart_add_url_is_resolved(self):
        url =reverse_lazy('orders:cart_add')
        self.assertEquals(resolve(url).func.view_class, CartAddView)
        
    def test_set_order_url_is_resolved(self):
        url =reverse_lazy('orders:set_order')
        self.assertEquals(resolve(url).func.view_class, SetOrderView)