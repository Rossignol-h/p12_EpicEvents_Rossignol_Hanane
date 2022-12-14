from rest_framework import serializers
from .models import Event


class PartialEventSerializer(serializers.ModelSerializer):
    client = serializers.ReadOnlyField(source='client.company_name', read_only=True)
    support_contact = serializers.ReadOnlyField(source='support_contact.email', read_only=True)

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ('id', 'support_contact', 'date_created', 'date_updated',)


class AllEventSerializer(serializers.ModelSerializer):
    client = serializers.ReadOnlyField(source='client.company_name', read_only=True)
    support_contact = serializers.ReadOnlyField(source='support_contact.email', read_only=True)

    class Meta:
        model = Event
        fields = "__all__"
