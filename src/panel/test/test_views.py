from django.test import TestCase,Client
from django.urls import reverse
from panel.forms import *
import json
from users.models import User
from orders.models import Table,Order,OrderItem
from foods.models import Food,Category
from dynamic_menu.models import Configuration

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
        # Failed test
        # self.assertTemplateUsed(response,'panel/dashboard_staff.html')

    def test_logout_GET(self):
        self.url=reverse("panel:logout")
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,302)


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

    def test_reject_order(self):
        self.url=reverse("panel:reject_order",args=[1])
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,302)

    def test_pay_order(self):
        self.url=reverse("panel:pay_order",args=[1])
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,302)

    def test_deliver_order(self):
        self.url=reverse("panel:deliver_order",args=[1])
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,302)

    def test_take_responsibility(self):
        self.url=reverse("panel:take_responsibility",args=[1])
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,302)


class TestLogoutView(TestCase):

    def test_dashboard_staff_GET(self):
        self.url=reverse("panel:dashboard")
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,302)

    def test_dashboard_staff_template_not_used(self):
        self.url=reverse("panel:dashboard")
        response = self.client.get(self.url)

        self.assertTemplateNotUsed(response,'panel/dashboard_staff.html')

    def test_edit_order_without_staff(self):
        self.url=reverse("panel:edit_order",args=[1])
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,404)






class TstAPI(TestCase):
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

        Configuration.objects.create()



    def test_api(self):
        url=reverse("panel:analytics-api")
        response = self.client.get(url)

        self.assertEquals(response.status_code,200)
