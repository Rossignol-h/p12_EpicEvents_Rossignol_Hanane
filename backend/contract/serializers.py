from rest_framework import serializers
from .models import Contract, ContractStatus


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"


class ContractStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContractStatus
        fields = "__all__"