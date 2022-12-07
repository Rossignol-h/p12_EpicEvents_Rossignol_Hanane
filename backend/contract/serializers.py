from rest_framework.serializers import ModelSerializer
from .models import Contract, ContractStatus

# ============================================= SERIALIZER FOR CREATE A CONTRACT


class ContractSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"

# ============================================= SERIALIZER FOR ALL SIGNED CONTRACTS


class ContractStatusSerializer(ModelSerializer):
    class Meta:
        model = ContractStatus
        fields = "__all__"