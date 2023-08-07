from django.contrib import admin
from .models import *
from . import models

# Register your models here.
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['title','description']

admin.site.register(Food)