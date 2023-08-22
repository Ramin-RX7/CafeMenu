from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import MainInfo, Social

class SingletonModelTestCase(TestCase):
    
    def test_maininfo_singleton(self):
        MainInfo.objects.create(title="Test", phone="1234567890", logo="path/to/logo.jpg", icon="path/to/icon.jpg")
        self.assertEqual(MainInfo.objects.count(), 1)        
        with self.assertRaises(ValidationError):
            MainInfo.objects.create(title="Test2", phone="0987654321", logo="path/to/logo2.jpg", icon="path/to/icon2.jpg")
        self.assertEqual(MainInfo.objects.count(), 1)        
        instance = MainInfo.objects.first()
        instance.delete()
        self.assertEqual(MainInfo.objects.count(), 1)

    def test_social_singleton(self):
        Social.objects.create()
        self.assertEqual(Social.objects.count(), 1)        
        with self.assertRaises(ValidationError):
            Social.objects.create()
        self.assertEqual(Social.objects.count(), 1)        
        instance = Social.objects.first()
        instance.delete()
        self.assertEqual(Social.objects.count(), 1)
