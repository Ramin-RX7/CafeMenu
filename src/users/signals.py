from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def apply_permissions(sender, **kwargs):
    if sender.label == apps.get_app_config('users'):
        from . import permissions
