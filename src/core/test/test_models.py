from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import models
from core.models import SingletonModel


# Create a concrete subclass of SingletonModel for testing purposes
class SingletonTestModel(SingletonModel):
    name = models.CharField(max_length=100)


class SingletonModelTest(TestCase):

    def test_only_one_instance_is_created(self):
        SingletonTestModel.objects.create(name="First Instance")
        self.assertEqual(SingletonTestModel.objects.count(), 1)

    def test_no_new_instance_allowed(self):
        SingletonTestModel.objects.create(name="First Instance")
        with self.assertRaises(ValidationError):
            SingletonTestModel.objects.create(name="Second Instance")
        self.assertEqual(SingletonTestModel.objects.count(), 1)

    def test_only_updates_to_existing_instance_are_allowed(self):
        first_instance = SingletonTestModel.objects.create(name="First Instance")
        existing_instance = SingletonTestModel.objects.first()
        existing_instance.name = "Updated Instance"
        existing_instance.save()
        self.assertEqual(SingletonTestModel.objects.first().name, "Updated Instance")
        new_instance = SingletonTestModel(name="New Instance")
        new_instance.pk = 123  # Setting a different pk
        with self.assertRaises(ValidationError):
            new_instance.save()

    def test_delete_method_does_nothing(self):
        SingletonTestModel.objects.create(name="First Instance")
        SingletonTestModel.objects.first().delete()
        self.assertEqual(SingletonTestModel.objects.count(), 1)
