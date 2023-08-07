from django.contrib import admin
from django.db.models.query import QuerySet
from datetime import datetime
from django.db.models import Q
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
        
class OrderStatusFilter(admin.SimpleListFilter):
    title = 'not paid'
    parameter_name = 'not paid'

    def lookups(self, request, model_admin):
        return[('not_paid','not_paid')]
    
    def queryset(self, request, queryset: QuerySet):
        if self.value() == 'not_paid':        
            return queryset.filter(~Q(status = 'Paid'))

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['customer','table','status','price','discount','final_price']
    ordering = ['created_at','updated_at']
    list_filter=[OrderToDayFilter,OrderStatusFilter]

@admin.register(models.Table)
class TableAdmin(admin.ModelAdmin):
    list_display=['name','is_reserved']
