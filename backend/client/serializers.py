from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Client


class ClientSerializer(ModelSerializer):
    sales_contact = serializers.ReadOnlyField(
        source='sales_contact.email', read_only=False)

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile',
                  'company_name', 'is_prospect', 'sales_contact', ]
