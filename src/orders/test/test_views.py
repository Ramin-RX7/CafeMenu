from django.test import TestCase, Client, RequestFactory
from django.urls import reverse, reverse_lazy
from orders.models import Table, Order, OrderItem
from users.models import User
from foods.models import Food, Category
from orders.views import IndexView, OrderDetailView, SetOrderView, cart
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
    
    def test_context_object_name_order_deatail_view(self):
        self.assertEquals(self.view_order_detail.model, Order)
        self.assertEquals(self.view_order_detail.context_object_name, 'order')
        self.assertEquals(self.view_order_detail.template_name, 'orders/order_details.html')
        
    def test_context_data_index_view(self):
        self.assertEquals(self.view_index.model, Order)
        
    def test_order_list_template_index_view(self):
        response = self.client.get(self.index_url)
        self.assertTemplateUsed(response, 'orders/order_list.html')
    
    def test_cart_template(self):
        response = self.client.get(self.cart_url)
        self.assertTemplateUsed(response, 'orders/cart.html')
      
    def test_valid_login_customer_login_view(self):
        valid_form_data = {'phone': '9176877108'}
        response = self.client.post(reverse('orders:customer_login'), data=valid_form_data)
        
        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.client.session.get('phone'), '9176877108')
           
    def test_invalid_login_customer_login_view(self):
        invalid_form_data = {'phone': '123456789'}
        response = self.client.post(reverse('orders:customer_login'), data=invalid_form_data)
        self.assertEqual(response.status_code, 302)
        
        import core.utils
        self.assertEquals(core.utils.EditableContexts.form_login_error, "Invalid phone number")
        
    def test_redirect_to_referer_customer_login_view(self):
        response = self.client.post(reverse('orders:customer_login'))
        self.assertRedirects(response, reverse('index'), target_status_code=200)
    
    
    def test_post_set_order_view(self):
        request = self.factory.post(reverse('orders:set_order'))
        request.COOKIES["cart"] = '{"' + str(self.food1.id) + '": 2}'
        request.session = {}
        request.session["phone"] = "9176877108"
        request.user = self.user1
        response = SetOrderView.as_view()(request)

        self.assertEqual(response.status_code, 302)
    
    def test_set_order_view_no_data(self):
        url = reverse("orders:set_order")  
        request = self.factory.post(url)
        response = SetOrderView.as_view()(request)
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(response.url, reverse("orders:cart"))
        # self.assertRedirects(response.url, reverse("orders:cart"))
    
    def test_post_set_order_view_no_customer_data(self):
        url = reverse("orders:set_order")  
        request = self.factory.post(url, data={"phone": "9176877108"}, COOKIES={"cart": "cart_data"})
        request.user = self.user1  
        request.session = {}
        response = SetOrderView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        expected_redirect_url = reverse("orders:cart")
        self.assertEqual(response.url, expected_redirect_url)
        
        # self.assertRedirects(response, expected_redirect_url)
    
    def test_cart_item_add_to_cart_view(self):
        initial_cart_data = {'food_1': 'quantity_1', 'food_2': 'quantity_2'}
        request = HttpRequest()
        request.COOKIES['cart'] = str(initial_cart_data)

        food_id_to_add = 'food_3'
        quantity_to_add = 'quantity_3'

        response = self.client.post(reverse('orders:cart_add'), data={'food': food_id_to_add, 'quantity': quantity_to_add}, cookies=request.COOKIES)
        self.assertEqual(response.status_code, 302)
        new_cart_data = eval(response.cookies['cart'].value)
        self.assertIn(food_id_to_add, new_cart_data)
        self.assertEqual(new_cart_data[food_id_to_add], quantity_to_add)
        self.assertRedirects(response, reverse('foods:menu'))
        
             
    
    # def test_get_object_order_detail_view(self):
        # request = self.factory.get(reverse('orders:order_details', args=[self.order1.id]))

        # session_middleware = SessionMiddleware(get_response=lambda r: HttpResponse())
        # session_middleware.process_request(request)
        # request.session['orders'] = [self.order1.id]  

        # view = OrderDetailView()
        # view.setup(request)
        # fetched_order = view.get_object()

        # self.assertEqual(fetched_order, self.order1)
        
   