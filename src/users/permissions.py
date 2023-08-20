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

permissions = Permission.objects.filter(codename__in=staff_permissions)
if not created:
    normal_staff.permissions.clear()
normal_staff.permissions.add(*permissions)



#> Manager
manager, created = Group.objects.get_or_create(name='Manager')

manager_excludes = [
    'delete_maininfo',
    'delete_social',
]
permissions = Permission.objects.exclude(codename__in=manager_excludes)
if not created:
    manager.permissions.clear()
manager.permissions.add(*permissions)



#> Super Staff
super_staff, created = Group.objects.get_or_create(name='Super Staff')

superstaff_permissions = [
    *staff_permissions,
    'change_maininfo',
    'change_social',
    'add_category',
    'change_category',
    'delete_category',
    'add_food',
    'change_food',
    'delete_food',
    'add_table',
    'change_table',
    'delete_table'
]
permissions = Permission.objects.filter(codename__in=superstaff_permissions)
if not created:
    super_staff.permissions.clear()
super_staff.permissions.add(*permissions)
