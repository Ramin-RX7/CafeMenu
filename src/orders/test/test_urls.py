from django.test import SimpleTestCase
from django.urls import reverse_lazy, resolve, reverse
from orders.views import OrderListView, IndexView, OrderDetailView, SetOrderView, CartAddView, CartDeleteView, CustomerLoginView, cart

class TestUrls(SimpleTestCase):
    def test_order_list_url_is_resolved(self):
        url =reverse_lazy('orders:order_list')
        # print(resolve(url))
        
        # view=resolve(url).func
        # self.assertEquals(view.__name__, OrderDetailView.as_view().__name__)

        self.assertEquals(resolve(url).func.view_class, OrderListView)
    