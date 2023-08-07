from django.contrib import admin
from .models import *
from . import models

# Register your models here.
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['title','description']
    ordering = ['title']

@admin.register(models.Food)
class FoodAdmin(admin.ModelAdmin):
    list_display=['title','price','discount','category','description']