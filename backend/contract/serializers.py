from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Contract, ContractStatus, ContractManager
# from authentication.models import Employee


class ContractManagerSerializer(ModelSerializer):
    class Meta:
        model = ContractManager
        # fields = ['id', 'sales_contact', 'contract__client.email', 'contract__payment_due', 'contract__status' ]
        fields = '__all__'


class ContractMemberSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
        # read_only_fields = ('amount',)


class ContractStatusSerializer(ModelSerializer):
    class Meta:
        model = ContractStatus
        fields = "__all__"