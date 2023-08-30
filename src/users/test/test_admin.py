from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from users.models import User
from users.admin import UserAdmin, UserStaffFilter, UserActiveFilter, SuperUserFilter
from users.forms import UserAddForm,ChangeForm

class MockSuperUser:
    def has_perm(self, perm):
        return True

request_factory = RequestFactory()
request = request_factory.get('/admin')
request.user = MockSuperUser()

class UserAdminTest(TestCase):
    
    def setUp(self):
        self.site = AdminSite()

        self.user = User.objects.create(
            phone='9123456789',
            first_name='test',
            last_name='testy',
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

    def test_user_staff_filter(self):
        ma = UserAdmin(User, self.site)
        filter_instance = UserStaffFilter(request, {}, User, ma)

        filter_instance.used_parameters = {'Staff': 'is_staff'}
        self.assertTrue(self.user in filter_instance.queryset(request, User.objects.all()))

        filter_instance.used_parameters = {'Staff': 'is_not_staff'}
        self.assertFalse(self.user in filter_instance.queryset(request, User.objects.all()))

    def test_user_active_filter(self):
        ma = UserAdmin(User, self.site)
        filter_instance = UserActiveFilter(request, {}, User, ma)

        filter_instance.used_parameters = {'Active/Inactive': 'active'}
        self.assertTrue(self.user in filter_instance.queryset(request, User.objects.all()))

        filter_instance.used_parameters = {'Active/Inactive': 'inactive'}
        self.assertFalse(self.user in filter_instance.queryset(request, User.objects.all()))

    def test_superuser_filter(self):
        ma = UserAdmin(User, self.site)
        filter_instance = SuperUserFilter(request, {}, User, ma)

        filter_instance.used_parameters = {'Superuser': 'superuser'}
        self.assertTrue(self.user in filter_instance.queryset(request, User.objects.all()))

    def test_get_form(self):
        ma = UserAdmin(User, self.site)
        
        self.assertEqual(ma.get_form(request), UserAddForm)
        self.assertEqual(ma.get_form(request, self.user), ChangeForm)
