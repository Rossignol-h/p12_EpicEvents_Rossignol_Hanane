from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import filters

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import Http404

from .serializers import ContractSerializer, UpdateContractSerializer, ContractStatusSerializer
from permissions import ObjectPermission
from .models import Contract, ContractStatus
from client.models import Client
from event.models import Event
from authentication.models import Employee


# =========================================================== CONTRACT VIEW


class ContractViewSet(viewsets.ModelViewSet):
    """
        Add, retrieve, update and delete a contract to the crm.
    """
    queryset = Contract.objects.all()
    permission_classes = [DjangoModelPermissions, ObjectPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['date_created', 'amount', 'client_id__email', 'client_id__company_name' ]

# ====================================================================== GET CONTRACTS OF AUTHENTICATED EMPLOYEE

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateContractSerializer
        else:
            return ContractSerializer

# ====================================================================== CUSTOM CREATE CONTRACT

    def create(self, request, *args, **kwargs):
        """
            Make sure that the sales_contact's contract
            is the one in charge of the client's contract 
        """
        
        employee = request.user
        if employee.role == 'sales':
            current_client = request.data['client']
            in_charge_of_client = Client.objects.filter(id=current_client, sales_contact=employee).first()

            if not in_charge_of_client:
                response = {'Sorry, You are not in charge of this client'}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
                
            else:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(sales_contact=employee)
                return Response({'new_contract': serializer.data,
                                'message':
                                f"This new contract is successfully added to the crm."},
                                status=status.HTTP_201_CREATED)


# ====================================================================== CUSTOM UPDATE CONTRACT


    def update(self, request, *args, **kwargs):
        """
            if user change status of contract to True (is signed),
            update the client status (he is not a prospect anymore),
            & add this contract to table "ContractStatus"
            & create an event.
        """
        current_contract = self.get_object()
        serializer = self.get_serializer(current_contract, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        

# ================================================================================ IF STATUS CHANGE UPDATE FOREIGN KEYS

        if serializer.data['status'] == True:
            signed_contract = ContractStatus.objects.filter(contract=current_contract)

            if not signed_contract:
                ContractStatus.objects.create(contract=current_contract)

                return Response({'new_contract': serializer.data,
                                    'message':
                                    f"This contract is successfully updated. Is signed and and ready to create an event"},
                                    status=status.HTTP_201_CREATED)
                
            else:
                return Response({'new_contract': serializer.data,
                                        'message':
                                        f"This contract is successfully updated."},
                                        status=status.HTTP_201_CREATED)

# ====================================================================== METHOD TO DISPLAY DELETE MESSAGE


    def destroy(self, request, *args, **kwargs):
        try:
            contract_to_delete = Contract.objects.get(id=self.kwargs['pk'])
            self.perform_destroy(contract_to_delete)
            return Response(
                        {'message': "This contract is successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            raise ValidationError("This contract doesn't exist")


# =========================================================== SIGNED CONTRACT VIEW


class ContractStatusViewSet(viewsets.ModelViewSet):
    """
    Read & retrieve all signed contracts.
    """
    serializer_class = ContractStatusSerializer
    queryset = ContractStatus.objects.all()
    permission_classes = [DjangoModelPermissions, ObjectPermission]
