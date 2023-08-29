from django.test import SimpleTestCase,TestCase
from panel.forms import *
from foods.models import *
from orders.models import Table


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



    def test_add_order_item_form(self):
        category=Category.objects.create(title="fastfood",description="",image="")
        food=Food.objects.create(title='pizza',description="",image="",price=10.55,discount=11.5,category=category,is_active=True)
        form = AddOrderItemForm(data={
            'quantity':2,
            'food':food
        })

        self.assertTrue(form.is_valid())


    def test_add_order_item_form_no_data(self):
        form = AddOrderItemForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),2)


    def test_edit_order_form(self):
        table=Table.objects.create(name='num1',is_reserved=False)
        form = EditOrderForm(data={
            'discount':20.2,
            'customer':'09125242979',
            'status':"Approved",
            'table':table
        })
        form.is_valid()

        self.assertTrue(form.is_valid())

    def test_edit_order_form_no_data(self):
        form= EditOrderForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),4)