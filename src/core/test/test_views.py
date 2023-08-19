from ..views import IndexTemplateView,AboutUsTemplateView
from django.test import TestCase
from django.urls import reverse


class IndexTemplateViewTest(TestCase):

    def test_url_exists(self):
        response=self.client.get('/')
        self.assertEqual(response.status_code,200)

    def test_url_available_by_name(self):
        response=self.client.get(reverse('index'))
        self.assertEqual(response.status_code,200)

    def test_template_name_correct(self):
        response=self.client.get(reverse('index'))
        self.assertTemplateUsed(response,'index.html')
    
    def test_template_content(self):
        response=self.client.get(reverse('index'))
        self.assertContains(response,'<h1 class="subtitle">Welcome To Our Restaurant</h1>')
        self.assertNotContains(response,'Not on the page')

    