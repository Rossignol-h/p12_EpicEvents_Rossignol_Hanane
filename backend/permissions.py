from django.contrib.auth.models import Group
from rest_framework import permissions


# ====================================== ADD AN EMPLOYEE TO GROUP PERMISSION


def add_to_group(new_employee):

    sales_group = Group.objects.get(name='sales')
    support_group = Group.objects.get(name='support')

    if new_employee.role == 'sales':
        new_employee.groups.add(sales_group)
    elif new_employee.role == 'support':
        new_employee.groups.add(support_group)

# ============================================ ERROR MESSAGES

NOT_ALLOWED = "You are not a manager !"

# ============================================ PERMISSION FOR EMPLOYEES


class EmployeePermission(permissions.BasePermission):
    """
        Check if the connected user is manager. 
    """
    
    def has_permission(self, request, view):
        self.message = NOT_ALLOWED

        if request.user.is_superuser:
            return True
        return False
