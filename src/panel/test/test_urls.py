from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import LoginView,UserVerifyView,logout,dashboard_staff,EditOrders,approve_order,reject_order,pay_order,deliver_order,take_responsibility
class TestUrls(SimpleTestCase):

    def test_login_url_is_resolved(self):
        url = reverse('panel:login')
        self.assertEquals(resolve(url).func.view_class,LoginView)

    def test_userverify_url_is_resolved(self):
        url = reverse('panel:user_verify')
        self.assertEquals(resolve(url).func.view_class,UserVerifyView)

    def test_logout_url_is_resolved(self):
        url = reverse('panel:logout')
        self.assertEquals(resolve(url).func,logout)

    def test_dashboard_url_is_resolved(self):
        url = reverse('panel:dashboard')
        self.assertEquals(resolve(url).func,dashboard_staff)

    def test_edit_order_url_is_resolved(self):
        url = reverse('panel:edit_order',args=[1])
        self.assertEquals(resolve(url).func.view_class,EditOrders)

    def test_approve_order_url_is_resolved(self):
        url = reverse('panel:approve_order',args=[1])
        self.assertEquals(resolve(url).func,approve_order)

    def test_reject_order_url_is_resolved(self):
        url = reverse('panel:reject_order',args=[1])
        self.assertEquals(resolve(url).func,reject_order)

    def test_pay_order_url_is_resolved(self):
        url = reverse('panel:pay_order',args=[1])
        self.assertEquals(resolve(url).func,pay_order)

    def test_deliver_order_url_is_resolved(self):
        url = reverse('panel:deliver_order',args=[1])
        self.assertEquals(resolve(url).func,deliver_order)