from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import MainInfo, Social

class MainInfoModelTest(TestCase):

    def setUp(self):
        self.logo = SimpleUploadedFile("logo.png", b"file_content", content_type="image/png")
        self.icon = SimpleUploadedFile("icon.png", b"file_content", content_type="image/png")

        self.main_info = MainInfo.objects.create(
            title="Test Title",
            motto="Test Motto",
            short_description="Test Short Description",
            about_us="Test About Us",
            phone="1234567890",
            email="test@example.com",
            logo=self.logo,
            icon=self.icon,
        )

    def test_main_info_str(self):
        self.assertEqual(str(self.main_info), "Main Info")

    def test_main_info_singleton(self):
        main_info_1 = MainInfo.objects.create(
            title="Test Title",
        )
        main_info_2 = MainInfo.objects.create(
            title="Another Title",
        )
        self.assertEqual(main_info_1, main_info_2)


class SocialModelTest(TestCase):

    def setUp(self):
        self.social = Social.objects.create(
            instagram="https://www.instagram.com/test/",
            telegram="https://t.me/test/",
            whatsapp="https://whatsapp.com/test/",
            youtube="https://www.youtube.com/test/",
            facebook="https://www.facebook.com/test/",
            tweeter="https://twitter.com/test/",
        )

    def test_social_str(self):
        self.assertEqual(str(self.social), "Social")

    def test_social_singleton(self):
        social_1 = Social.objects.create(
            instagram="https://www.instagram.com/test/",
        )
        social_2 = Social.objects.create(
            instagram="https://www.instagram.com/another/",
        )

        self.assertEqual(social_1, social_2)


