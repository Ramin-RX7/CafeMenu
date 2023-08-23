from django.test import SimpleTestCase
from panel.forms import *


class TestForms(SimpleTestCase):

    def test_user_login_form(self):
        form = UserLogInForm(data={
            "phone":"09125242979"
        })

        self.assertTrue(form.is_valid())