from django.contrib import admin
from .models import MainInfo,Social


@admin.register(MainInfo)
class MainInfoAdmin(admin.ModelAdmin):
    exclude = ("id",)
    list_display = ('title',)


@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    exclude = ("id",)
