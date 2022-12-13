from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import filters
from django.conf import settings

from .serializers import EmployeeSerializer
from permissions import EmployeePermission
from .models import Employee

User = settings.AUTH_USER_MODEL


# =========================================================== EMPLOYEE VIEW


class EmployeeViewSet(viewsets.ModelViewSet):
    """
        Add, retrieve, update and delete an employee instance.
    """
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = [DjangoModelPermissions, EmployeePermission]
    search_fields = ['email', 'role']
    filter_backends = (filters.SearchFilter,)

# =========================================================== OVERRIDE DELETE EMPLOYEE

    def destroy(self, request, *args, **kwargs):
        try:
            employee_to_delete = Employee.objects.get(id=self.kwargs['pk'])

            if employee_to_delete == request.user:
                return Response(
                    {'message': "You can not delete yourself !"},
                    status=status.HTTP_403_FORBIDDEN)

            if employee_to_delete.id == 1:
                return Response(
                    {'message': "You can not delete the first manager !"},
                    status=status.HTTP_403_FORBIDDEN)

            self.perform_destroy(employee_to_delete)
            return Response(
                {'message': "This employee is successfully deleted"},
                status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            raise ValidationError("This employee doesn't exist")
