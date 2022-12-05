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
NOT_IN_CHARGE = "You are not in charge of this !"

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

# ============================ PERMISSION FOR CLIENTS & CONTRACTS


class ObjectPermission(permissions.BasePermission):
    """ 
        Check if the connected user
        is the main contact in charge of this contract or client;
    """

    def has_object_permission(self, request, view, obj):
        superuser_or_manager = [
        request.user.is_superuser, 
        request.user.role == 'management',
        request.user.groups.filter(name='management')
        ]
        self.message = NOT_IN_CHARGE

        if view.action in ['retrieve','update'] and request.user == obj.sales_contact_id:
            return True

        elif request.user in superuser_or_manager:
            return True

        else:
            return False

# ============================ PERMISSION FOR EVENTS
