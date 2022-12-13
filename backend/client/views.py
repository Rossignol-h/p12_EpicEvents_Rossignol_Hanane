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
    search_fields = ['company_name','email']


# ====================================================================== DISABLE LIST ACTION FOR THIS VIEW


    def create(self, request, *args, **kwargs):
        """
            If the request user is a sales employee :
                save this client, and add him as sales_contact.
            If the request user is superuser(manager),
                the sales_contact will be chosen by himself
        """
        employee = self.request.user
        serializer = self.get_serializer(data=request.data)

        if employee.is_superuser:
            try:
                if request.data['sales_contact'] is None:
                    raise Exception()
                else:
                    serializer.is_valid(raise_exception=True)
                    new_client = serializer.save()
            except Exception:
                raise ValidationError("As manager you have to specifiy a sales_contact")

        elif employee.role == 'sales':
            serializer.is_valid(raise_exception=True)
            new_client = serializer.save(sales_contact=employee)

        return Response({'new_client': self.serializer_class(new_client,
                            context=self.get_serializer_context()).data,
                            'message':
                            f"This new client is successfully added to the crm."},
                            status=status.HTTP_201_CREATED)


# ====================================================================== METHOD TO DISPLAY DELETE MESSAGE


    def destroy(self, request, *args, **kwargs):
        """
            Displays a success message to the frontend.
        """
        try:
            client_to_delete = Client.objects.get(id=self.kwargs['pk'])
            self.perform_destroy(client_to_delete)
            return Response(
                        {'message': "This client is successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            raise ValidationError("This client doesn't exist")
