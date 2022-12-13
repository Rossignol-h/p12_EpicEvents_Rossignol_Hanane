from rest_framework import serializers
from .models import Event


class PartialEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ('id', 'support_contact', 'date_created', 'date_updated',) 


class AllEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
