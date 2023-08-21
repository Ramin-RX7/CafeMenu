from ..forms import UserAddForm,UserChangeForm
from django.test import TestCase
from ..models import User


class UserAddFormTest(TestCase):
    def test_fields_correct(self):
        form=UserAddForm()
        expected_fields=['phone', 'first_name', 'last_name', 'is_staff', 'is_active','password1','password2']
        self.assertEqual(list(form.fields),expected_fields)

    def test_username_lastname_required(self):
        form_data={
            'phone':'9121111222',
            'is_staff':True,
            'is_active':True,
            'password1':'testpassword123',
            'password2':'testpassword123'
        }

        form=UserAddForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_not_same_password(self):
        form_data={
            'phone':'9121111222',
            'first_name':'test', 
            'last_name':'testpoor',
            'is_staff':True,
            'is_active':True,
            'password1':'testpassword',
            'password2':'testpassword123'
        }

        form=UserAddForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserChangeFormTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user=User.objects.create_user(phone='9124567890',password='testpassword')    

    def test_fields_correct(self):
        form=UserChangeForm(instance=self.user)
        expected_fields=['phone', 'first_name', 'last_name', 'is_staff', 'is_active','password']
        self.assertEqual(list(form.fields),expected_fields)

    def test_firstname_lastname_required(self):
        form_data={
            'phone': '9124567890',
            'is_staff': False,
            'is_active': False
        }
        form=UserChangeForm(data=form_data,instance=self.user)
        self.assertTrue(form.is_valid())

    def test_password_cleaning(self):
        form_data= {
            'phone': '9124567890',
            'password': 'newpassword',
            'is_staff': False,
            'is_active': False
        }
        form=UserChangeForm(data=form_data,instance=self.user)
        self.assertTrue(form.is_valid())
        self.assertTrue(self.user.check_password('newpassword'))

