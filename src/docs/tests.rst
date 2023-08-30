Tests
=====

We have many test for our project and you can see all of them in test folders in every apps.

For example this test about url test:

``` class TestUrls(SimpleTestCase):

    def test_login_url_is_resolved(self):
        url = reverse('panel:login')
        self.assertEquals(resolve(url).func.view_class,LoginView)```


Command for running test:

```python manage.py test panel.test```

Tip 1: for linux user, you should use (python3) alternative (python) at first of command


