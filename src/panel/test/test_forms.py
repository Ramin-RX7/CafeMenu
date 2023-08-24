from django.test import SimpleTestCase,TestCase
from panel.forms import *
from foods.models import *


class TestForms(TestCase):

    def test_user_login_form(self):
        form = UserLogInForm(data={
            "phone":"09125242979"
        })

        self.assertTrue(form.is_valid())

    def test_user_login_form_no_data(self):
        form = UserLogInForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),1)



    def test_user_verify_form(self):
        form = UserVerifyForm(data={
            'otp':1222
        })

        self.assertTrue(form.is_valid())


    def test_user_verify_form_no_data(self):
        form = UserVerifyForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),1)


    def test_edit_order_item_form(self):
        category=Category.objects.create(title="fastfood",description="",image="")
        food=Food.objects.create(title='pizza',description="",image="",price=10.55,discount=11.5,category=category,is_active=True)
        form = EditOrderItemForm(data={
            'id':5,
            'quantity':2,
            'food':food
        })

        self.assertTrue(form.is_valid())


    def test_edit_order_item_form_no_data(self):
        form = EditOrderItemForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),2)
