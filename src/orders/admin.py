from django.contrib import admin
from django.db.models.query import QuerySet
from datetime import datetime
from .models import *
from . import models

class OrderToDayFilter(admin.SimpleListFilter):
    title = 'Date'
    parameter_name = 'Date'

    def lookups(self, request, model_admin):
        return[('today','today')]
    
    def queryset(self, request, queryset: QuerySet):
        if self.value() == 'todaye':
            return queryset.filter(created_at = datetime.today())

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['customer','table','status','price','discount','final_price']
    ordering = ['created_at','updated_at']
    list_filter=[OrderToDayFilter]

@admin.register(models.Table)
class TableAdmin(admin.ModelAdmin):
    list_display=['name','is_reserved']
