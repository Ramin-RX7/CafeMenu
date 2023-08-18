from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import LoginView,UserVerifyView,logout,dashboard_staff,EditOrders,approve_order,reject_order,pay_order,deliver_order,take_responsibility
class TestUrls(SimpleTestCase):

    def test_login_url_is_resolved(self):
        url = reverse('panel:login')
        self.assertEquals(resolve(url).func.view_class,LoginView)

