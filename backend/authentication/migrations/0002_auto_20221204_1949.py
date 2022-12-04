from django.db import migrations

def create_groups(apps, schema_migration):
    """
        migration for automatically creating groups for a given schema
    """

    Employee = apps.get_model('authentication', 'Employee')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    add_client = Permission.objects.get(codename='add_client')
    change_client = Permission.objects.get(codename='change_client')
    view_client = Permission.objects.get(codename='view_client')

    add_contract = Permission.objects.get(codename='add_contract')
    change_contract = Permission.objects.get(codename='change_contract')
    view_contract = Permission.objects.get(codename='view_contract')

    add_contractstatus = Permission.objects.get(codename='add_contractstatus')
    change_contractstatus = Permission.objects.get(codename='change_contractstatus')
    view_contractstatus = Permission.objects.get(codename='view_contractstatus')

    add_event = Permission.objects.get(codename='add_event')
    change_event = Permission.objects.get(codename='change_event')
    view_event = Permission.objects.get(codename='view_event')

# =============================================== SALES PERMISSIONS

    sales_permissions = [
        add_client, change_client, view_client,
        add_contract, change_contract, view_contract,
        add_contractstatus, change_contractstatus, view_contractstatus,
        add_event, view_event
    ]

    sales_group = Group(name='sales')
    sales_group.save()
    sales_group.permissions.set(sales_permissions)


# =============================================== SUPPORT PERMISSIONS


    support_permissions = [
        view_client, view_contract,
        change_event, view_event
    ]

    support_group = Group(name='support')
    support_group.save()
    support_group.permissions.set(support_permissions)

# =============================================== SET EACH PERMISSIONS

    for user in Employee.objects.all():
        if user.role == 'sales':
            user.groups.add(sales_group)
        elif user.role == 'support':
            user.groups.add(support_group)

# =============================================== MIGRATION


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]
