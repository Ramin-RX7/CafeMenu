from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import models
from core.models import BaseModel
from django.utils import timezone
from foods.models import Category
import datetime


class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Test Category", description="This is a test category")

    def test_created_at_field(self):
        self.assertIsNotNone(self.category.created_at)
        self.assertTrue(timezone.now() - self.category.created_at < datetime.timedelta(seconds=5))

    def test_updated_at_field(self):
        self.assertIsNotNone(self.category.updated_at)
        self.assertTrue(timezone.now() - self.category.updated_at < datetime.timedelta(seconds=5))
        self.category.description = "Updated test category"
        self.category.save()
        self.category.refresh_from_db()
        self.assertTrue(timezone.now() - self.category.updated_at < datetime.timedelta(seconds=5))
