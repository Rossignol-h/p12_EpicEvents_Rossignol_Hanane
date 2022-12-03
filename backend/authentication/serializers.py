from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'email','password', 'phone_number','role','groups', 'is_staff', 'is_superuser']
        read_only_fields = ['is_staff', 'is_superuser', 'groups']

    def validate(self, data):
        """
            Check that email ends with @epicevent.com.
        """
        if not data['email'].endswith('@epicevents.com'):
            raise serializers.ValidationError("Wrong email format: Please make sure to write @epicevent.com")
        return data

    def create(self, validated_data):
        return Employee.objects.create_user(**validated_data)
