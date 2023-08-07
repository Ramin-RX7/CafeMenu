from typing import Any, List, Optional, Tuple
from django.contrib import admin
from django.db.models.query import QuerySet
from . import models

class CategoryFilter(admin.SimpleListFilter):
    title = 'Empty Category'
    parameter_name = 'title'

    def lookups(self, request, model_admin):
        return[('title','Categories')]
    
    def queryset(self, request, queryset: QuerySet):
        if self.value() == 'title':
            return queryset.filter(food = None)

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['title','created_at','updated_at']
    ordering = ['title']
    search_fields = ['title']
    list_filter = [CategoryFilter]

@admin.register(models.Food)
class FoodAdmin(admin.ModelAdmin):
    list_display=['title','price','discount','category', 'created_at']
    ordering = ['title']
    search_fields = ['title','category']
