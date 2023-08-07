from django.contrib import admin
from .models import *
from . import models

# Register your models here.
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['customer','table','status','price','discount']

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=['order','food','quantity','unit_price','discount']

admin.site.register(Table)
