from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import models
from core.models import SingletonModel,BaseModel
from django.utils import timezone


# # Create a concrete subclass of SingletonModel for testing purposes
# class SingletonTestModel(SingletonModel):
#     name = models.CharField(max_length=100)


# class SingletonModelTest(TestCase):

#     def test_only_one_instance_is_created(self):
#         SingletonTestModel.objects.create(name="First Instance")
#         self.assertEqual(SingletonTestModel.objects.count(), 1)

#     def test_no_new_instance_allowed(self):
#         SingletonTestModel.objects.create(name="First Instance")
#         with self.assertRaises(ValidationError):
#             SingletonTestModel.objects.create(name="Second Instance")
#         self.assertEqual(SingletonTestModel.objects.count(), 1)

#     def test_only_updates_to_existing_instance_are_allowed(self):
#         first_instance = SingletonTestModel.objects.create(name="First Instance")
#         existing_instance = SingletonTestModel.objects.first()
#         existing_instance.name = "Updated Instance"
#         existing_instance.save()
#         self.assertEqual(SingletonTestModel.objects.first().name, "Updated Instance")
#         new_instance = SingletonTestModel(name="New Instance")
#         new_instance.pk = 123  # Setting a different pk
#         with self.assertRaises(ValidationError):
#             new_instance.save()

#     def test_delete_method_does_nothing(self):
#         SingletonTestModel.objects.create(name="First Instance")
#         SingletonTestModel.objects.first().delete()
#         self.assertEqual(SingletonTestModel.objects.count(), 1)


# class BaseModelTest(TestCase):

    # class TempModel(BaseModel):
    #     name = models.CharField(max_length=100)

    # def test_created_at_and_updated_at(self):
    #     instance = self.TempModel(name="Test")
    #     instance.save()

    #     instance = self.TempModel.objects.get(pk=instance.pk)

    #     # Testing that created_at and updated_at were set upon creation.
    #     self.assertIsNotNone(instance.created_at)
    #     self.assertIsNotNone(instance.updated_at)
    #     self.assertAlmostEqual(instance.created_at, timezone.now(), delta=timezone.timedelta(seconds=2))
    #     self.assertAlmostEqual(instance.updated_at, timezone.now(), delta=timezone.timedelta(seconds=2))

    #     time_to_wait = timezone.timedelta(seconds=2)
    #     timezone.sleep(time_to_wait.total_seconds())

    #     instance.name = "Updated Test"
    #     instance.save()

    #     instance = self.TempModel.objects.get(pk=instance.pk)

    #     # Testing that updated_at was updated upon saving the model again.
    #     self.assertGreater(instance.updated_at, instance.created_at)


# class BaseModelTest(TestCase):
#     def test_created_at_auto_now_add(self):
#         test = BaseModel.objects.create()
#         self.assertIsNotNone(test.created_at)

#     def test_updated_at_auto_now(self):
#         test = BaseModel.objects.create()
#         current_time = timezone.now()
#         test.save()
#         self.assertGreaterEqual(test.updated_at, test.created_at)
#         self.assertGreaterEqual(test.updated_at, current_time)

#     def test_updated_at_changes_on_update(self):
#         test = BaseModel.objects.create()
#         initial_updated_at = test.updated_at
#         timezone.now()
#         test.save()
#         self.assertNotEqual(test.updated_at, initial_updated_at)
