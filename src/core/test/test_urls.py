from django.urls import reverse, resolve
from django.test import SimpleTestCase
from ..views import AboutUsTemplateView, IndexTemplateView

class URLTestCase(SimpleTestCase):
    
    def test_about_us_url(self):
        url = reverse('about_us')
        self.assertEqual(url, '/about/')
        resolved = resolve('/about/')
        self.assertEqual(resolved.func.view_class, AboutUsTemplateView)

    def test_index_url(self):
        url = reverse('index')
        self.assertEqual(url, '/')
        resolved = resolve('/')
        self.assertEqual(resolved.func.view_class, IndexTemplateView)
