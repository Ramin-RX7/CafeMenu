from django.test import TestCase,Client
from django.urls import reverse
from panel.forms import *
import json
from users.models import User
from orders.models import Table,Order,OrderItem
from foods.models import Food,Category

class TestViews(TestCase):


    def test_login_template(self):
        self.url=reverse("panel:login")
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'panel/login.html')


    def test_login_GET(self):
        self.url=reverse("panel:login")
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,200)


    def test_user_verify_GET(self):
        self.url=reverse("panel:user_verify")
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,302)


    def test_dashboard_staff_GET(self):
        self.url=reverse("panel:dashboard")
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,302)

    def test_logout_GET(self):
        self.url=reverse("panel:logout")
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,302)


class TestLoginView(TestCase):
    def setUp(self):
        User.objects.create_superuser(phone='09123456789',password='1234')
        self.client= Client()
        self.client.login(phone='09123456789',password='1234')

    def test_dashboard_staff_GET(self):
        self.url=reverse("panel:dashboard")
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,200)

    def test_dashboard_staff_template(self):
        self.url=reverse("panel:dashboard")
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'panel/dashboard_staff.html')




class TestEditOrder(TestCase):
    def setUp(self):
        User.objects.create_superuser(phone='09123456789',password='1234')
        self.client= Client()
        self.client.login(phone='09123456789',password='1234')

        self.category= Category.objects.create(
            title='Iranian Foods'
        )

        self.food = Food.objects.create(
            title='Kabab',
            price=10,
            category=self.category
        )

        self.table = Table.objects.create(
            name='table 1',
            is_reserved=False,
        )

        self.user = User.objects.create(
            phone="9176877108",
            first_name = 'Ali',
            last_name= 'Afzal',
            is_active=True,
            is_staff=False,
        )

        self.order = Order(
            customer='9176877108',
            table=self.table,
            discount=2.5,
            responsible_staff=self.user,
        )
        self.order.save(check_items=False)

        self.order_item = OrderItem.objects.create(
            order=self.order,
            food=self.food,
            unit_price=self.food.price,
            quantity=4,
            discount=0.0,
            )


    def test_edit_order(self):
        self.url=reverse("panel:edit_order",args=[1])
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,200)

    def test_approve_order(self):
        self.url=reverse("panel:approve_order",args=[1])
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,302)


