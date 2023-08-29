from django.test import TestCase,Client
from django.urls import reverse
from panel.forms import *
import json
from users.models import User

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