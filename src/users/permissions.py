from django.contrib.auth.models import Group,Permission



#> Normal staff
normal_staff, created = Group.objects.get_or_create(name='Normal Staff')

staff_permissions = [
    'view_user',
    'view_order',
    'change_order',
    'view_food',
    'view_maininfo',
    'view_socials',
    'view_category',
    'view_table',
]

permissions = Permission.objects.filter(codename__in=permission_codenames)

normal_staff.permissions.clear()
normal_staff.permissions.add(*permissions)
