from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import filters
from django.conf import settings

from .serializers import ClientSerializer
from permissions import ObjectPermission
from .models import Client

User = settings.AUTH_USER_MODEL


# =========================================================== CLIENT VIEW


class ClientViewSet(viewsets.ModelViewSet):
    """
        Add, retrieve, update and delete client to the crm.
    """
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [DjangoModelPermissions, ObjectPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['company_name', 'is_prospect', 'email']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_client = serializer.save(sales_contact=request.user)

        return Response({'new_client': ClientSerializer(new_client,
                            context=self.get_serializer_context()).data,
                            'message':
                            f"This new client is successfully added to the crm."},
                            status=status.HTTP_201_CREATED)


    def destroy(self, request, *args, **kwargs):
        try:
            client_to_delete = Client.objects.get(id=self.kwargs['pk'])
            self.perform_destroy(client_to_delete)
            return Response(
                        {'message': "This client is successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            raise ValidationError("This client doesn't exist")
