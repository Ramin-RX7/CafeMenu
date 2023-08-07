from django.contrib import admin
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html

from . import models
from .forms import FoodForm, CategoryForm



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
    list_display=['title','view_foods','created_at','updated_at']
    ordering = ['title']
    search_fields = ['title']
    list_filter = [CategoryFilter]


    def view_foods(self, obj):
        url = reverse(f'admin:{models.Food._meta.app_label}_{models.Food._meta.model_name}_changelist')
        link = f'<a href="{url}?category__id__exact={obj.pk}">View Foods</a>'
        return format_html(link)
    view_foods.short_description = 'Foods'
    readonly_fields = ('view_foods',)

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return super().get_fieldsets(request, obj)
        return  (
            ('Category Details', {
                'fields': ('title', 'description', 'image'),
            }),
            ('Associated Foods', {
                'fields': ('view_foods',),
            }),
        )

    form = CategoryForm

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('delete_image'):
            obj.image.delete()
        super().save_model(request, obj, form, change)



@admin.register(models.Food)
class FoodAdmin(admin.ModelAdmin):
    list_display=['title','price','discount','category', 'created_at']
    ordering = ['title']
    search_fields = ['title','category']

    form = FoodForm

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('delete_image'):
            obj.image.delete()
        super().save_model(request, obj, form, change)
