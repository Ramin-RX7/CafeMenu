from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.urls import reverse

from ..admin import UserAdmin

CustomUser = get_user_model()
class UserAdminTest(TestCase):


    @classmethod
    def setUpTestData(cls):
        cls.user1 = CustomUser.objects.create(first_name='John', last_name='Doe', phone='09121234567')
        cls.user2 = CustomUser.objects.create(first_name='Jane', last_name='Doe', phone='09122314567')
        cls.admin_user = CustomUser.objects.create_superuser(phone='09121234568', password='adminpassword')

    def setUp(self):
        self.client.login(phone='09121234568', password='adminpassword')  

    def test_search(self):
        response = self.client.get(reverse('admin:users_user_changelist'), {'q': 'John'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertNotContains(response, 'Jane Doe')

    def test_user_staff_filter(self):
        response = self.client.get(reverse('admin:users_user_changelist'), {'Staff': 'is_staff'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'Jane Doe')

    def test_user_active_filter(self):
        response = self.client.get(reverse('admin:users_user_changelist'), {'Active/Inactive': 'active'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'Jane Doe')

    def test_superuser_filter(self):
        response = self.client.get(reverse('admin:users_user_changelist'), {'Superuser': 'superuser'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.admin_user.phone) 

    def test_change_form(self):
        response = self.client.get(reverse('admin:users_user_add'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First name:')
        self.assertContains(response, 'Last name:')
        self.assertContains(response, 'Phone:')

    def test_change_user(self):
        response = self.client.get(reverse('admin:users_user_change', args=(self.user1.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

    def test_change_user_form(self):
        response = self.client.get(reverse('admin:users_user_change', args=(self.user1.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First name:')
        self.assertContains(response, 'Last name:')
        self.assertContains(response, 'Phone:')

    def test_add_user(self):
        response = self.client.get(reverse('admin:users_user_add'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First name:')
        self.assertContains(response, 'Last name:')
        self.assertContains(response, 'Phone:')
