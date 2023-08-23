from django.test import TestCase,Client
from django.urls import reverse
from panel.forms import *
import json


class TestViews(TestCase):

    def test_login_template(self):
        self.url=reverse("panel:login")
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'panel/login.html')


    def test_login_GET(self):
        self.url=reverse("panel:login")
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,200)

    # def test_login_POST(self):
    #     self.url=reverse("panel:login")
    #     phone = "09123456789"

    # def test_call_view_fail_blank(self):
    #     self.client.login(usename="09125242979")
    #     response = self.client.post(reverse("panel:login"), {})
    #     self.assertFormError(response, 'UserLogInForm', 'some_field')

    def test_user_verify_GET(self):
        self.url=reverse("panel:user_verify")
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,302)

    # def test_dashboard_staff_template(self):
    #     self.url=reverse("panel:dashboard")
    #     response = self.client.get(self.url)

    #     self.assertTemplateUsed(response,'panel/dashboard_staff.html')

    def test_dashboard_staff_GET(self):
        self.url=reverse("panel:dashboard")
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,302)

    def test_logout_GET(self):
        self.url=reverse("panel:logout")
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,302)


