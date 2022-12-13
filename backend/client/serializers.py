from rest_framework.serializers import ModelSerializer
from .models import Client


class ClientSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['id','first_name','last_name', 'email', 'phone', 'mobile',
                'company_name', 'is_prospect', 'sales_contact', ]
