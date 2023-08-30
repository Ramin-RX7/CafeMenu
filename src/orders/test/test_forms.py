from django.test import SimpleTestCase
from orders.forms import CustomerLoginForm, PhoneInput

class TestForms(SimpleTestCase):    
    def test_customer_login_form_valid_data(self):
        form = CustomerLoginForm(data={
            'phone' : '123456789',
        })
        self.assertFalse(form.is_valid())
        
    def test_customer_login_form_no_data(self):
        form = CustomerLoginForm(data={})
        
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
    
    def test_phone_input_attrs(self):
        widget = PhoneInput()

        self.assertIn('class', widget.attrs)
        self.assertEqual(widget.attrs['class'], 'form-control')
    