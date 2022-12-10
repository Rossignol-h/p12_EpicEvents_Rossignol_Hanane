from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Contract, ContractStatus

# ======================================================================== SERIALIZER FOR CREATE A CONTRACT


class ContractSerializer(ModelSerializer):
    sales_contact = serializers.ReadOnlyField(source='sales_contact.email', read_only=True)

    class Meta:
        model = Contract
        fields = ('id', 'amount', 'payment_due', 'status', 'date_created', 'date_updated', 'client', 'sales_contact', ) 

# ======================================================================== SERIALIZER FOR ALL SIGNED CONTRACTS


class ContractStatusSerializer(ModelSerializer):
    class Meta:
        model = ContractStatus
        fields = "__all__"
