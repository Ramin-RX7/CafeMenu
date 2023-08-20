from django.test import Client, TestCase
from django.urls import reverse_lazy, resolve, reverse
from orders.views import OrderListView, IndexView, OrderDetailView, SetOrderView, CartAddView, CartDeleteView, CustomerLoginView, cart

class TestUrls(TestCase):
    def setUp(self):
        self.client = Client()
        # self.order_list = reverse('order_list')
        self.cart = reverse('orders:cart')
    
    def test_order_list_url_is_resolved(self):
        url =reverse_lazy('orders:order_list')
        # print(resolve(url))
        
        # view=resolve(url).func
        # self.assertEquals(view.__name__, OrderDetailView.as_view().__name__)

        self.assertEquals(resolve(url).func.view_class, OrderListView)
    
    # def test_order_details_url_is_resolved(self):
    #     order_id = '123'
    #     url =reverse_lazy('orders:order_details', args=['order_id'])
    #     self.assertEquals(resolve(url).func.view_class, OrderDetailView)
        
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