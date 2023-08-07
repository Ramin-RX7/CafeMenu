from django.contrib import admin
from . import models
from django.db.models.query import QuerySet

class UserFilter(admin.SimpleListFilter):
    title = 'Staff'
    parameter_name = 'Staff'

    def lookups(self, request, model_admin):
        return[('is_staff','is_staff'),('is_not_staff','is_not_staff')]
    
    def queryset(self, request, queryset: QuerySet):
        if self.value() == 'is_not_staff':
            return queryset.filter(is_staff = False)
        if self.value() == 'is_staff':
            return queryset.filter(is_staff = True)
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['first_name','last_name','phone']
    list_filter = [UserFilter]
