from rest_framework.serializers import ModelSerializer
from .models import Employee


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'email','password', 'phone_number','role','groups', 'is_staff', 'is_superuser']
        read_only_fields = ['is_staff', 'is_superuser', 'groups']

    def create(self, validated_data):
        return Employee.objects.create_user(**validated_data)
