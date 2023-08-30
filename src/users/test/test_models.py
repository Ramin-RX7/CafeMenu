from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import User
from core.validators import phone_validator
from django.db import IntegrityError


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


class UserTestCase(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(
            phone='9123456789',
            password='passwordtest',
            first_name='test',
            last_name='testy',
        )
    

    def test_user_create(self):
        self.assertIsInstance(self.user,User)


    def test_unique_phone(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                phone='9123456789',
                password='passpass',
                first_name='1test',
                last_name='1testy',
            )

    def test_valid_phone_validator(self):
        valid_phones=[
            '9123456789',
            '+989123456789',
            '00989123456789',
            '09123456789'
        ]
        for phone in valid_phones:
            with self.subTest(phone=phone):
                self.assertIsNotNone(phone_validator(phone))

    def test_wrong_phones(self):

        invalid_phones=[
            '123',
            '123456789123456789',
            '91234567891234567',
            '912345678',
            '',
            'None'
        ]
        for phones in invalid_phones:
            with self.assertRaises(ValidationError):
                phone_validator(phones)


    def test_user_fields(self):
        self.assertEqual(self.user.phone, '9123456789')
        self.assertEqual(self.user.first_name, 'test')
        self.assertEqual(self.user.last_name, 'testy')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)




