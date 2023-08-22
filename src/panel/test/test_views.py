from django.test import TestCase,Client
from django.urls import reverse
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

