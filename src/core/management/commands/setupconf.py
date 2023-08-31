from django.core.management.base import BaseCommand
from dynamic_menu.models import Configuration,Social,MainInfo


class Command(BaseCommand):
    help = 'Create required configs/models before first run'

    def handle(self, *args, **options):
        if not Configuration.objects.exists():
            Configuration.objects.create()
        from users import permissions
