from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['title','created_at','updated_at']
    ordering = ['title']

@admin.register(models.Food)
class FoodAdmin(admin.ModelAdmin):
    list_display=['title','price','discount','category', 'created_at']
    ordering = ['title','price']
    search_fields = ['title','category']
