from django.contrib.auth.models import Group


# ====================================== ADD AN EMPLOYEE TO GROUP PERMISSION


def add_to_group(new_employee):

    sales_group = Group.objects.get(name='sales')
    support_group = Group.objects.get(name='support')

    if new_employee.role == 'sales':
        new_employee.groups.add(sales_group)
    elif new_employee.role == 'support':
        new_employee.groups.add(support_group)
