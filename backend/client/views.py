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
from contract.models import Contract
from event.models import Event

User = settings.AUTH_USER_MODEL

# =========================================================== READ CONTRACT VIEW


# class ReadClientsView(viewsets.ReadOnlyModelViewSet):
#     """
#     List all clients with restricted informations.
#     """
#     serializer_class = ClientListSerializer
#     queryset = Client.objects.all()
#     permission_classes = [DjangoModelPermissions, ObjectPermission]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['email', 'company_name' ]

# # ====================================================================== DISABLE RETRIEVE ACTION FOR THIS VIEW

#     def retrieve(self, request, pk=None):
#         response = {'message': 'Retrieve method not allowed, please go to this endpoint crm/client/client_id/'}
#         return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


    # def list(self, request, pk=None):
    #     if self.request.META['QUERY_STRING'].startswith('search='):
    #         response = ("je suis dans le true")
    #     else:
    #         response = ("je suis dans le else")
    #     return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


    # def get_queryset(self):
    #     if self.request.META['QUERY_STRING'].startswith('search='):
    #         client_of_user = Client.objects.filter(sales_contact=self.request.user)
    #         if client_of_user.count() > 1:
    #             return client_of_user
    #         else : 
    #             return ObjectPermission
    #     else:
    #         return Client.objects.all()
            
    # def get_object(self):
        # return super().get_object()       
        
        # if self.request.query_params.get('search'):
        # if self.request.query_params.get('search'):
        # if '?search=' in self.request.get_full_path():
            # if "/home/1" == request.get_full_path
        # if self.request.META['QUERY_STRING'].startswith('search='):
        #     employee = self.request.user
        # obj = self.get_queryset()
        # if obj is not None:
        #     self.check_object_permissions(self.request, obj)
        #     return obj
        # else:
        #     return self.permission_classes.ObjectPermission
        
        
        
        

# =========================================================== CLIENT VIEW


class ClientViewSet(viewsets.ModelViewSet):
    """
        Add, retrieve, update and delete client to the crm.
    """
    serializer_class = ClientSerializer
    # queryset = Client.objects.all()
    permission_classes = [DjangoModelPermissions, ObjectPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['company_name','email']


# ====================================================================== DISABLE LIST ACTION FOR THIS VIEW


    # def list(self, request, pk=None):

    #     response = {'message': 'List method not allowed, please go to this endpoint crm/clients/'}
    #     return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# ====================================================================== GET ALL CLIENTS OF AUTHENTICATED EMPLOYEE

    def get_queryset(self):
        employee = self.request.user
        if employee.role == 'sales':
            try: 
                client_of_current_employee = Client.objects.filter(sales_contact=employee)
                if client_of_current_employee:
                    return client_of_current_employee
            except:
                return Client.objects.none()
            
            # except ObjectDoesNotExist:
                # raise ValidationError("Sorry, Currently You have no clients")
        
        # elif employee.role == 'support':
        #     return Client.event_set.filter(support_contact=employee)

        if employee.role == 'support':
            clients = [e.client.id for e in Event.objects.filter(support_contact=employee)]
            for client in clients:
                return Client.objects.filter(id=client)

        elif employee.is_superuser:
            return Client.objects.all()
        else:
            return Client.objects.none()


# ====================================================================== CUSTOM CREATE CLIENT


    def create(self, request, *args, **kwargs):
        """
            save this client, and adding the user of the request as 
            sales_contact.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_client = serializer.save(sales_contact=request.user)

        return Response({'new_client': ClientDetailSerializer(new_client,
                            context=self.get_serializer_context()).data,
                            'message':
                            f"This new client is successfully added to the crm."},
                            status=status.HTTP_201_CREATED)


# ====================================================================== CUSTOM UPDATE CLIENT


    def update(self, request, *args, **kwargs):
        """
            Make sure the 'is_prospect' attribute is set to false
            if this client exist in a contract,
            because is not a prospect anymore.
        """
        current_client = self.get_object()

        # clients_in_contract = Contract.objects.get().client_contract.filter(id=current_client.id)
        clients_in_contract = Contract.objects.filter(client=current_client.id)
        if clients_in_contract is not None:
            request.data['is_prospect'] = "False"

        serializer = self.get_serializer(current_client, data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(serializer.data)

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
