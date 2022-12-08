from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Client


class ClientListSerializer(ModelSerializer):
    sales_contact = serializers.ReadOnlyField(source='sales_contact.email', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'company_name', 'is_prospect', 'sales_contact']


class ClientDetailSerializer(ModelSerializer):
    sales_contact = serializers.ReadOnlyField(source='sales_contact.email', read_only=True)

    class Meta:
        model = Client
        fields = ['id','first_name','last_name', 'email', 'phone', 'mobile',
                'company_name', 'is_prospect', 'sales_contact', ]
