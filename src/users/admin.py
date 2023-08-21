from django.contrib import admin
from django.db.models.query import QuerySet

from . import models
from .forms import UserAddForm,ChangeForm



class UserStaffFilter(admin.SimpleListFilter):
    title = 'Staff'
    parameter_name = 'Staff'
    def lookups(self, request, model_admin):
        return [('is_staff','is_staff'),('is_not_staff','is_not_staff')]
    def queryset(self, request, queryset: QuerySet):
        if self.value() == 'is_not_staff':
            return queryset.filter(is_staff = False)
        if self.value() == 'is_staff':
            return queryset.filter(is_staff = True)

class UserActiveFilter(admin.SimpleListFilter):
    title='Active/Inactive'
    parameter_name = 'Active/Inactive'
    def lookups(self, request, model_admin):
        return [('active','active'),('inactive','inactive')]
    def queryset(self, request, queryset: QuerySet):
        if self.value() == 'active':
            return queryset.filter(is_active=True)
        if self.value() == 'inactive':
            return queryset.filter(is_active=False)

class SuperUserFilter(admin.SimpleListFilter):
    title='Superuser'
    parameter_name = 'Superuser'
    def lookups(self, request, model_admin):
        return [('superuser','superuser')]
    def queryset(self, request, queryset: QuerySet):
        if self.value() == 'superuser':
            return queryset.filter(is_superuser =True)


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['first_name','last_name','phone']
    list_filter = [UserStaffFilter,UserActiveFilter,SuperUserFilter]

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return UserAddForm
        else:
            return ChangeForm
