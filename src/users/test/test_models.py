from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import User
from core.validators import phone_validator


class UserManagerTestCase(TestCase):

    def test_create_user(self):
        phone='9123456789'
        password='testpassword'
        user=User.objects.create_user(phone=phone, password=password)
        self.assertEqual(user.phone,phone)
        self.assertTrue(user.check_password(password))

    def test_create_user_without_phone(self):
        phone=None
        password='testpassword'
        with self.assertRaises(ValueError):
            user=User.objects.create_user(phone=phone,password=password)
        

    def test_set_password(self):
        user=User.objects.create_user(phone='9123456789', password='testpassword')
        user.set_password('newpassword')
        user.save()
        self.assertTrue(user.check_password('newpassword'))

    def test_create_superuser_staff_true(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                phone='9123456789',
                password='superpassword',
                is_staff=False 
            )
    
    def test_create_superuser_true(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(phone='9123456789',
                                          password='password',
                                          is_superuser=False)



class PhoneNumberFieldTestCase(TestCase):

    def test_get_prep_wrong_value(self):
        value='011122345678'
        with self.assertRaises(ValidationError):
            regex = phone_validator(value)

    def test_get_prep_value(self):
        value='9123456789'
        regex = phone_validator(value)
        phone_parts = regex.groupdict()
        self.assertEqual(phone_parts["operator"],'912')
        self.assertEqual(phone_parts['middle3'],'345')
        self.assertTrue(phone_parts['last4'],'6789')


    def test_get_phone(self):
        value='00989123456789'
        regex = phone_validator(value)
        phone_parts = regex.groupdict()
        phone = phone_parts["operator"]+phone_parts["middle3"]+phone_parts["last4"]
        self.assertEqual(phone,'9123456789')



