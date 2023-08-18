from users.models import *
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

class UserModelTest(TestCase):
    def setUp(self) -> None:
        self.user_data={
            'phone':'9121111555',
            'first_name':'test',
            'last_name':'test'
        }


    def create_user_test(self):
        user = User.objects.create_user(**self.user_data, password='testpass')
        self.assertTrue(user.check_password('testpass'))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active) 

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(**self.user_data, password='testpass')
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_active)

    def test_create_user_missing_phone(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(phone=None, password='testpass')

    def test_create_superuser_non_staff(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(is_staff=False, password='testpass', **self.user_data)

    def test_create_superuser_non_superuser(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(is_superuser=False, password='testpass', **self.user_data)

    def test_phone_number_field_prep_value(self):
        phone_field = User._meta.get_field('phone')
        prepped_value = phone_field.get_prep_value('1234567890')
        self.assertEqual(prepped_value, '1234567890')

    def test_phone_number_field_prep_value(self):
        phone_field = User._meta.get_field('phone')
        valid_phone = '9124567890'
        expected_formatted_phone = '912-456-7890'
        prepped_valid = phone_field.get_prep_value(valid_phone)
        self.assertEqual(prepped_valid, valid_phone)





