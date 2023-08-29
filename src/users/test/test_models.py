from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import User


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


