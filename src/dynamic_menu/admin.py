from django.contrib import admin
from .models import MainInfo,Social,Configuration


@admin.register(MainInfo)
class MainInfoAdmin(admin.ModelAdmin):
    exclude = ("id",)
    list_display = ('title',)


@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    exclude = ("id",)


@admin.register(Configuration)
class ConfigurationsAdmin(admin.ModelAdmin):
    exclude = ("id",)
