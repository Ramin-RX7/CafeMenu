from django.contrib import admin
from .models import *
from . import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['customer','table','status','price','discount','final_price']


@admin.register(models.Table)
class TableAdmin(admin.ModelAdmin):
    list_display=['name','is_reserved']
