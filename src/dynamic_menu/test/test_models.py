from django.test import TestCase
from dynamic_menu.models import MainInfo,Social

class MainInfoModelTest(TestCase):
    def test_create_instance(self):
        main_info = MainInfo.objects.create(
            title="Test Title",
            motto="Test Motto",
            short_description="Test Description",
            about_us="Test About Us",
            phone="1234567890",
            email="test@email.com",
            logo="images/dynamic_menu/test_logo.png",
            icon="images/dynamic_menu/test_icon.png"
        )
        self.assertEqual(str(main_info), "Main Info")

    def test_str_method(self):
        main_info = MainInfo.objects.create(title="Test Title")
        self.assertEqual(str(main_info), "Main Info")


class SocialModelTest(TestCase):
    def test_create_instance(self):
        social = Social.objects.create(
            instagram="test_instagram",
            telegram="test_telegram",
            whatsapp="test_whatsapp",
            youtube="test_youtube",
            facebook="test_facebook",
            tweeter="test_tweeter"
        )
        self.assertEqual(social.instagram, "test_instagram")
        self.assertEqual(social.telegram, "test_telegram")
