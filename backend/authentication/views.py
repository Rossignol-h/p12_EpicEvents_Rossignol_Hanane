from rest_framework import viewsets
from rest_framework import filters
from django.conf import settings

from .serializers import EmployeeSerializer
from .models import Employee

User = settings.AUTH_USER_MODEL


# =========================================================== EMPLOYEE VIEW


class EmployeeViewSet(viewsets.ModelViewSet):
    """
        Add, retrieve, update and delete an employee instance.
    """

    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = []
    search_fields = ['email', 'role']
    filter_backends = (filters.SearchFilter,)
